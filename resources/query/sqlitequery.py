
GET_ALL = (""" 
    SELECT * FROM "tbReadedBarcode"
""")  

CHECK_BARCODE = (""" 
    SELECT "documentNo" FROM "tbReadedBarcode" WHERE "documentNo" = ?
""")

ADD_BARCODE = (""" 
    INSERT INTO "tbReadedBarcode"
    ("documentNo", "date", "status")
    VALUES (?, (SELECT DATETIME('now', 'localtime')), 'KONTROL EDİLDİ')
""")

COUNT_BARCODE = (""" 
    SELECT COUNT (*) FROM "tbReadedBarcode"
""")

DELETE_BARCODES = (""" 
    DELETE FROM "tbReadedBarcode"
""")