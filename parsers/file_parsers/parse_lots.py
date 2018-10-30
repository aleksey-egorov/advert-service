#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django
import sys
import logging
import time
import glob
import mimetypes
import pandas as pd
from django.utils import timezone
from django.db import transaction
from optparse import OptionParser

sys.path.append("/work/advert")   # Django root folder
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advert.settings")
django.setup()

from lot.models import Lot, Currency, LotGallery
from product.models import Product
from brand.models import Brand
from supplier.models import SupplierOrg, Supplier
from geo.models import Region
from user.models import User

PARSER_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print (PARSER_BASE_DIR)



def read_files(pattern):
    '''Чтение файлов с лотами и списка фотографий'''
    dfs = []
    raw_names = []
    for fn in glob.iglob(os.path.join("data", pattern)):
        logging.info('Processing %s' % fn)

        df = pd.read_excel(fn, header=0, names=['num', 'user_id', 'suporg', 'supplier', 'lotname', 'active', 'best', 'category',
                                        'brand', 'model', 'price', 'currency', 'manuf_year', 'region', 'state', 'description'])
        _, fname = os.path.split(fn)
        name, _ = os.path.splitext(fname)
        image_filenames = check_images(name)

        dfs.append((df, image_filenames))
        raw_names.append(name)
    return dfs, raw_names


def check_images(name):
    '''Проверка фотографий лотов в папке'''
    image_filenames = {}
    dirname = os.path.join("data", name + "_images")
    logging.info("Checking images in {}".format(dirname))
    if os.path.exists(dirname):
        for ldir in os.listdir(dirname):
            imdir = os.path.join(dirname, ldir)
            images = []
            for image in os.listdir(imdir):
                full_path = os.path.abspath(os.path.join(imdir, image))
                if mimetypes.guess_type(full_path)[0] == 'image/jpeg':
                    images.append(full_path)
            if len(images) > 0:
                image_filenames[int(ldir)] = images
    return image_filenames


def load_dataframes(dfs):
    '''Обработка dataframe'''
    total_parse_errors = 0
    total_add_errors = 0
    processed = 0

    for item in dfs:
        df, image_filenames = item
        i = 0
        running = True
        while running:
            if not df.num[i] >= 0:
                break
            lot, parse_errors = parse_row(df, i)
            add_errors = 0
            if parse_errors == 0:
                add_errors = add_lot(lot, image_filenames)
            total_parse_errors += parse_errors
            total_add_errors += add_errors
            processed += 1
            i += 1
    return processed, total_parse_errors, total_add_errors


def parse_row(df, i):
    '''Парсинг одной строки в dict'''
    lot = {'suporg': None, 'supplier': None, 'price': None, 'manuf_year': None}
    errors = 0
    lot['list_num'] = int(df.num[i])

    try:
        lot['user'] = User.objects.get(id=df.user_id[i])
    except:
        logging.exception("Row {}: bad user_id - {}".format(i, df.user_id[i]))
        errors += 1

    try:
        lot['suporg'] = SupplierOrg.objects.get(name=df.suporg[i])
    except:
        logging.exception("Row {}: bad supplier_org - {}".format(i, df.suporg[i]))
        errors += 1

    try:
        if not lot['suporg'] == None:
            lot['supplier'] = Supplier.objects.get(name=df.supplier[i], org=lot['suporg'])
        else:
            lot['supplier'] = Supplier.objects.get(name=df.supplier[i])
    except:
        logging.exception("Row {}: bad supplier - {}".format(i, df.supplier[i]))
        errors += 1

    lot['lotname'] = df.lotname[i]
    if df.active[i] in ('TRUE','True', 'да'):
        lot['active'] = True
    else:
        lot['active'] = False

    if df.best[i] in ('TRUE', 'True', 'да'):
        lot['best'] = True
    else:
        lot['best'] = False

    try:
        lot['brand'] = Brand.objects.get(name=df.brand[i])
    except:
        logging.exception("Row {}: bad brand - {}".format(i, df.brand[i]))
        errors += 1

    try:
        lot['product'] = Product.objects.get(name=df.model[i])
    except:
        logging.exception("Row {}: bad product - {}".format(i, df.model[i]))
        errors += 1

    if df.price[i] > 0:
        lot['price'] = df.price[i]
    try:
        lot['currency'] = Currency.objects.get(name=df.currency[i])
    except:
        logging.exception("Row {}: bad currency - {}".format(i, df.currency[i]))
        errors += 1

    if df.manuf_year[i] > 0:
        lot['manuf_year'] = df.manuf_year[i]

    try:
        lot['region'] = Region.objects.get(name=df.region[i])
    except:
        logging.exception("Row {}: bad region - {}".format(i, df.model[i]))
        errors += 1

    if df.state[i] in ('Новый', 'новый'):
        lot['new_prod_state'] = True
    else:
        lot['new_prod_state'] = False

    lot['description'] = df.description[i]

    return lot, errors


def add_lot(lot, filenames):
    '''Добавление лота и фотографий'''
    errors = 0
    with transaction.atomic():
        new_lot = None
        try:
            new_lot = Lot(
                name=lot['lotname'],
                product=lot['product'],
                supplier=lot['supplier'],
                price=lot['price'],
                currency=lot['currency'],
                main_description=lot['description'],
                active=lot['active'],
                new_prod_state=lot['new_prod_state'],
                best=lot['best'],
                add_date=timezone.now(),
                upd_date=timezone.now(),
                main_image=None,
                manuf_year=lot['manuf_year'],
                region=lot['region'],
                author=lot['user']
            )
            new_lot.save()
            alias, num = Lot.objects._make_num_alias(new_lot.name, new_lot.id)
            new_lot.alias = alias
            new_lot.num = num
            new_lot.save()
        except Exception as err:
            logging.exception("Error adding lot: {}".format(err))
            errors += 1

        print("FNAMES: {}".format(lot['list_num']))
        try:
            num = 0

            for full_imagepath in filenames[lot['list_num']]:
                filename = new_lot.alias + "_" + str(num) + ".jpg"
                LotGallery.objects._move_image_from_location(full_imagepath, filename)
                LotGallery.objects._update_image(new_lot, num, filename)
                LotGallery.objects._update_main_image(new_lot)
                num += 1
        except Exception as err:
            logging.exception("Error adding images: {}".format(err))
            errors += 1

    logging.info("Added lot {}".format(new_lot.num))
    return errors


def move_data(raw_names):
    for name in raw_names:
        oldpath = os.path.join(PARSER_BASE_DIR, 'data', name + '.xlsx')
        newpath = os.path.join(PARSER_BASE_DIR, 'complete', name + '.xlsx')
        os.rename(oldpath, newpath)

        oldpath = os.path.join(PARSER_BASE_DIR, 'data', name + '_images')
        newpath = os.path.join(PARSER_BASE_DIR, 'complete', name + '_images')
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        files = os.listdir(oldpath)
        for f in files:
            oldfile = os.path.join(oldpath, f)
            newfile = os.path.join(newpath, f)
            os.rename(oldfile, newfile)


def main(opts):
    dfs,raw_names = read_files(opts.pattern)
    processed, total_parse_errors, total_add_errors = load_dataframes(dfs)
    logging.info("Loading complete: processed={} parse_errors={} add_errors={}".format(processed, total_parse_errors, total_add_errors))
    move_data(raw_names)


if __name__ == '__main__':
    op = OptionParser()
    op.add_option("-l", "--log", action="store", default=None)
    op.add_option("--dry", action="store_true", default=False)
    op.add_option("--pattern", action="store", default="*.xlsx")

    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO if not opts.dry else logging.DEBUG,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

    logging.info("Starting file parser with options: %s" % opts)
    start_time = time.time()
    try:
        #opts.workers = int(opts.workers)
        main(opts)
    except Exception as e:
        logging.exception("Unexpected error: %s" % e)
        sys.exit(1)
    finally:
        elapsed_time = time.time() - start_time
        logging.info("Time elapsed: %s sec" % elapsed_time)
        print("Work finished")
    sys.exit(0)
