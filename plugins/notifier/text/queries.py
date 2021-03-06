#!/usr/local/opt/python/libexec/bin/python
# -*- coding: utf-8 -*-

# Collection of sqlite queries to be used by messages-notifier.py


def get_sqlite_attach_db_query(username, contact_db_dir):
    return "ATTACH '/Users/%s/Library/Application Support/AddressBook/Sources/%s/AddressBook-v22.abcddb' as adb" % (
        username, contact_db_dir)

# query for copy/paste to SQLite console
"""
SELECT
    rcrd.*,
    msg.guid as id, 
    cht.rowid as rowid, 
    cht.guid as cguid, 
    cht.chat_identifier as cid, 
    cht.group_id as grp, 
    cht.display_name as title, 
    strftime(
        '%m-%d-%Y %H:%M:%S', 
        datetime(date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime')
    ) as timestamp, 
    CASE 
        WHEN instr(hdl.id, '@') > 0 
        THEN hdl.id 
        ELSE substr(hdl.id, -10) 
    END contact, 
    substr(replace(replace(replace(replace(pnmbr.ZFULLNUMBER, '-', ''), ' ', ''), '(', ''), ')', ''), -10) as phone, 
    replace(
        CASE 
            WHEN rcrd.ZLASTNAME IS NULL 
            THEN rcrd.ZFIRSTNAME 
            ELSE rcrd.ZFIRSTNAME 
            || ' ' || 
            CASE 
                WHEN rcrd.ZMIDDLENAME IS NULL 
                THEN '' 
                ELSE rcrd.ZMIDDLENAME 
            END 
            || ' ' || 
            rcrd.ZLASTNAME 
        END, '  ', ' ') as sender, 
    rcrd.ZORGANIZATION as org, 
    msg.cache_has_attachments, 
    atc.mime_type, 
    atc.filename, 
    replace(replace(text, CHAR(10), ' '), CHAR(13), ' ') as message 
FROM message msg 
INNER JOIN handle hdl 
    ON hdl.ROWID = msg.handle_id
LEFT JOIN chat_message_join cmj 
    ON msg.rowid = cmj.message_id 
LEFT JOIN chat cht 
    ON cmj.chat_id = cht.rowid 
LEFT JOIN message_attachment_join maj 
    ON (msg.rowid = maj.message_id AND msg.cache_has_attachments = 1) 
LEFT JOIN attachment atc 
    ON maj.attachment_id = atc.rowid 
LEFT JOIN adb.ZABCDPHONENUMBER pnmbr 
    ON contact = phone 
LEFT JOIN adb.ZABCDEMAILADDRESS eml 
    ON contact = eml.ZADDRESSNORMALIZED
LEFT JOIN adb.ZABCDRECORD as rcrd 
    ON (pnmbr.ZOWNER = rcrd.Z_PK OR eml.ZOWNER = rcrd.Z_PK)
WHERE is_read = 0 
    AND text != 'NULL' 
    AND is_from_me != 1 
ORDER BY date;
"""

sqlite_select_query = "SELECT " \
                        "msg.guid as id, " \
                        "cht.rowid as rowid, " \
                        "cht.guid as cguid, " \
                        "cht.chat_identifier as cid, " \
                        "cht.group_id as grp, " \
                        "cht.display_name as title, " \
                        "strftime(" \
                          "'%m-%d-%Y %H:%M:%S', " \
                          "datetime(date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime')" \
                        ") as timestamp, " \
                        "CASE " \
                          "WHEN instr(hdl.id, '@') > 0 " \
                          "THEN hdl.id " \
                          "ELSE substr(hdl.id, -10) " \
                        "END contact, " \
                        "substr(" \
                          "replace(" \
                            "replace(" \
                              "replace(" \
                                "replace(" \
                                  "pnmbr.ZFULLNUMBER, '-', ''), ' ', ''), '(', ''), ')', ''), -10" \
                        ") as phone, " \
                        "replace(" \
                          "CASE " \
                            "WHEN rcrd.ZLASTNAME IS NULL " \
                            "THEN rcrd.ZFIRSTNAME " \
                            "ELSE rcrd.ZFIRSTNAME " \
                              "|| ' ' || " \
                              "CASE " \
                                "WHEN rcrd.ZMIDDLENAME IS NULL " \
                                "THEN '' " \
                                "ELSE rcrd.ZMIDDLENAME " \
                              "END " \
                              "|| ' ' || " \
                              "rcrd.ZLASTNAME " \
                          "END, '  ', ' ') as sender, " \
                        "rcrd.ZORGANIZATION as org, " \
                        "msg.cache_has_attachments, " \
                        "atc.mime_type, " \
                        "atc.filename, " \
                        "replace(replace(text, CHAR(10), ' '), CHAR(13), ' ') as message " \
                      "FROM message msg " \
                      "INNER JOIN handle hdl " \
                        "ON hdl.ROWID = msg.handle_id " \
                      "LEFT JOIN chat_message_join cmj " \
                        "ON cmj.message_id = msg.rowid " \
                      "LEFT JOIN chat cht " \
                        "ON cht.rowid = cmj.chat_id " \
                      "LEFT JOIN message_attachment_join maj " \
                        "ON (maj.message_id = msg.rowid AND msg.cache_has_attachments = 1) " \
                      "LEFT JOIN attachment atc " \
                        "ON atc.rowid = maj.attachment_id " \
                      "LEFT JOIN adb.ZABCDPHONENUMBER pnmbr " \
                        "ON phone = contact " \
                      "LEFT JOIN adb.ZABCDEMAILADDRESS eml " \
                        "ON eml.ZADDRESSNORMALIZED = contact " \
                      "LEFT JOIN adb.ZABCDRECORD as rcrd " \
                        "ON (rcrd.Z_PK = pnmbr.ZOWNER OR rcrd.Z_PK = eml.ZOWNER) " \
                      "WHERE is_read = 0 " \
                        "AND text != 'NULL' " \
                        "AND is_from_me != 1 " \
                      "ORDER BY date "

sqlite_get_recent_query = "SELECT " \
                          "msg.guid as id, " \
                          "cht.rowid as rowid, " \
                          "cht.guid as cguid, " \
                          "cht.chat_identifier as cid, " \
                          "cht.group_id as grp, " \
                          "cht.display_name as title, " \
                          "strftime(" \
                            "'%m-%d-%Y %H:%M:%S', " \
                            "datetime(date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime')" \
                          ") as timestamp, " \
                          "CASE " \
                            "WHEN instr(hdl.id, '@') > 0 " \
                            "THEN hdl.id " \
                            "ELSE substr(hdl.id, -10) " \
                          "END contact, " \
                          "substr(" \
                            "replace(" \
                              "replace(" \
                                "replace(" \
                                  "replace(" \
                                    "pnmbr.ZFULLNUMBER, '-', ''), ' ', ''), '(', ''), ')', ''), -10" \
                          ") as phone, " \
                          "replace(" \
                            "CASE " \
                              "WHEN rcrd.ZLASTNAME IS NULL " \
                              "THEN rcrd.ZFIRSTNAME " \
                              "ELSE rcrd.ZFIRSTNAME " \
                                "|| ' ' || " \
                                "CASE " \
                                  "WHEN rcrd.ZMIDDLENAME IS NULL " \
                                  "THEN '' " \
                                  "ELSE rcrd.ZMIDDLENAME " \
                                "END " \
                                "|| ' ' || " \
                                "rcrd.ZLASTNAME " \
                            "END, '  ', ' ') as sender, " \
                          "rcrd.ZORGANIZATION as org, " \
                          "msg.cache_has_attachments, " \
                          "atc.mime_type, " \
                          "atc.filename, " \
                          "replace(replace(text, CHAR(10), ' '), CHAR(13), ' ') as message " \
                        "FROM message msg " \
                        "INNER JOIN handle hdl " \
                          "ON hdl.ROWID = msg.handle_id " \
                        "LEFT JOIN chat_message_join cmj " \
                          "ON cmj.message_id = msg.rowid " \
                        "LEFT JOIN chat cht " \
                          "ON cht.rowid = cmj.chat_id " \
                        "LEFT JOIN message_attachment_join maj " \
                          "ON (maj.message_id = msg.rowid AND msg.cache_has_attachments = 1) " \
                        "LEFT JOIN attachment atc " \
                          "ON atc.rowid = maj.attachment_id " \
                        "LEFT JOIN adb.ZABCDPHONENUMBER pnmbr " \
                          "ON phone = contact " \
                        "LEFT JOIN adb.ZABCDEMAILADDRESS eml " \
                          "ON eml.ZADDRESSNORMALIZED = contact " \
                        "LEFT JOIN adb.ZABCDRECORD as rcrd " \
                          "ON (rcrd.Z_PK = pnmbr.ZOWNER OR rcrd.Z_PK = eml.ZOWNER) " \
                        "WHERE text != 'NULL' " \
                        "ORDER BY date " \
                        "DESC " \
                        "LIMIT 100 "

sqlite_group_chat_query = "SELECT " \
                            "cht.chat_identifier as cid, " \
                            "strftime(" \
                              "'%m-%d-%Y %H:%M:%S', " \
                              "datetime(date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime')" \
                            ") as timestamp, " \
                            "CASE " \
                              "WHEN instr(hdl.id, '@') > 0 " \
                              "THEN hdl.id " \
                              "ELSE substr(hdl.id, -10) " \
                            "END contact, " \
                            "substr(" \
                              "replace(" \
                                "replace(" \
                                  "replace(" \
                                    "replace(" \
                                      "pnmbr.ZFULLNUMBER, '-', ''), ' ', ''), '(', ''), ')', ''), -10" \
                            ") as phone, " \
                            "replace(" \
                              "CASE " \
                                "WHEN rcrd.ZLASTNAME IS NULL " \
                                "THEN rcrd.ZFIRSTNAME " \
                                "ELSE rcrd.ZFIRSTNAME " \
                                  "|| ' ' || " \
                                  "CASE " \
                                    "WHEN rcrd.ZMIDDLENAME IS NULL " \
                                    "THEN '' " \
                                    "ELSE rcrd.ZMIDDLENAME " \
                                  "END " \
                                  "|| ' ' || " \
                                  "rcrd.ZLASTNAME " \
                              "END, '  ', ' ') as sender, " \
                            "rcrd.ZORGANIZATION as org " \
                          "FROM message msg " \
                          "INNER JOIN handle hdl " \
                            "ON hdl.ROWID = msg.handle_id " \
                          "LEFT JOIN adb.ZABCDPHONENUMBER pnmbr " \
                            "ON phone = contact " \
                          "LEFT JOIN adb.ZABCDEMAILADDRESS eml " \
                            "ON eml.ZADDRESSNORMALIZED = contact " \
                          "LEFT JOIN adb.ZABCDRECORD as rcrd " \
                            "ON (rcrd.Z_PK = pnmbr.ZOWNER OR rcrd.Z_PK = eml.ZOWNER) " \
                          "LEFT JOIN chat_message_join cmj " \
                            "ON cmj.message_id = msg.rowid " \
                          "LEFT JOIN chat cht " \
                            "ON cht.rowid = cmj.chat_id " \
                          "WHERE cht.chat_identifier = ? " \
                          "ORDER BY date " \
                          "DESC " \
                          "LIMIT ? "

# sqlite_query_order_by = "ORDER BY strftime('%m-%d-%Y %H:%M:%S', datetime(date/1000000000 + " \
#                         "strftime('%s', '2001-01-01') ,'unixepoch','localtime'))"
