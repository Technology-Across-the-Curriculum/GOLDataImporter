# GOLDataTool

## GOLDataParser

GOLDataParser is a python scrip that traverses a structured directory containing  TurningPoint session files and Grade/Consent files and parses the direcotres in to course section object. 

## GOLDataImporter

GOLDataImporter is a python reads an output directory with Pickel object files that contain the informaion parsed from the GOLDataParse and imports the informaion into the reserach databases schemea.

## GOLDClassroster

GOLDClassroster is a python script that parses a .xlsx that contas a sheet 'G' (grades) and 'C' (consenters) then matches student records between the two and saves those resultds in new sheet 'M' (matched).
