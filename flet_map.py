import requests


link = "https://wxs.ign.fr/topographie/geoportail/tms/1.0.0/BDTOPO/metadata.json/"

# a = requests.get(link).json()
# for key, value in a.items():
#     print(key)


key = "clccdcfyr98kxbex3eevvopi"
link2 = f"https://wxs.ign.fr/{key}/geoportail/wmts?" + \
        "&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0"# +\
    #     "&STYLE=normal" +\
    #     "&TILEMATRIXSET=PM" +\
    #     "&FORMAT=image/jpeg"+\
    #     "&LAYER=ORTHOIMAGERY.ORTHOPHOTOS"+\
	# "&TILEMATRIX={z}" +\
    #     "&TILEROW={y}" +\
    #     "&TILECOL={x}"

a = requests.get(link2)
print(a)
# print(type(a.json()))