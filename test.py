from amazon.Database import Database

cursor = Database.cursor()
# with open(item['code'] + '.txt', 'w+') as the_file:
#     the_file.write(item['code'] + '\n')
cursor.execute("""
UPDATE codes set html='%s' where code = '%s'
""" % ('somehtml', '0007411820'))
cursor.connection.commit()