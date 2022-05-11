from file_importer import FileImporter

importer = FileImporter('../Sketch-Data-master/SketchData/Domain01')
data = importer.get_data()
print(data)
