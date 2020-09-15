import os

class AcvReporter(object):
    ''' Generates AcvReporter.smali classes.
    '''

    def __init__(self, classes_info):
        self.classes_info = classes_info
        self.number_of_fields = len(self.classes_info)
        return
    
    @staticmethod
    def get_reporter_field(class_name, class_number):
        field_name = Smali.get_reporting_field_name(class_name, class_number)
        return "Ltool/acv/AcvReporter;->{}".format(field_name)
    
    def get_reporting_class(self):
        fields = []
        init_arrays = []
        i = 0
        for name, length, number in self.classes_info:
            field_name = Smali.get_reporting_field_name(name, number)
            fields.append(Smali.get_acv_static_field(name, number))
            init_block = Smali.get_clinit_array(hex(length), field_name)
            init_arrays.append(init_block)
            i += 1
        reporter_fields = "\n".join(fields)
        init_arrays = "\n".join(init_arrays)
        reporter = Smali.get_reporter_smali(reporter_fields, init_arrays)
        saving_arrays = self.get_saving_all_arrays()
        reporter += Smali.get_saving_method_smali(self.number_of_fields, saving_arrays)
        return reporter

    def get_saving_all_arrays(self):
        arrays = []
        i = 0
        for name, length, number in self.classes_info:
            arrays.append(Smali.get_save_array_smali(hex(i), name, number))
            i += 1
        all_arrays = "\n".join(arrays)
        return all_arrays
        
    def save_file(self, dir_path, reporter):
        reporter_dir = os.path.join(dir_path, 'tool', 'acv')
        reporter_path = os.path.join(reporter_dir, Smali.ACVREPORTER_FILENAME)
        if not os.path.isdir(reporter_dir):
            os.makedirs(reporter_dir)
        with open(reporter_path, 'w') as f_writer:
            f_writer.write(reporter)

    def save(self, dir_path):
        reporter = self.get_reporting_class()
        self.save_file(dir_path, reporter)


class Smali(object):
    ''' AcvReport specific smali manipulations.
    '''

    ACVREPORTER_FILENAME = "AcvReporter.smali"

    @staticmethod
    def get_reporting_field_name(class_name, class_number):
        return "{}{}".format(''.join(class_name[:-1].split('/')), class_number)

    @staticmethod
    def get_save_array_smali(hex_i, class_name, class_number):
        field = Smali.get_reporting_field_name(class_name, class_number)
        return Smali.SAVE_ARRAY_SMALI.format(index=hex_i, field=field)

    @staticmethod
    def get_acv_static_field(class_name, class_number):
        field_name = Smali.get_reporting_field_name(class_name, class_number)
        return ".field public static {}:[Z".format(field_name)

    @staticmethod
    def get_clinit_array(hex_len, field_name):
        return Smali.CLINIT_SMALI.format(hex_len, field_name)

    @staticmethod
    def get_reporter_smali(fields, field_inits):
        return Smali.REPORTER_SMALI.format(fields=fields, field_inits=field_inits)

    @staticmethod
    def get_saving_method_smali(number_of_fields, arrays):
        return Smali.SAVE_EXTERNAL_FILE_SMALI.format(number=hex(number_of_fields), arrays=arrays)


    SAVE_ARRAY_SMALI = r'''
const/16 v3, {index}
sget-object v4, Ltool/acv/AcvReporter;->{field}:[Z 
aput-object v4, v0, v3
'''

    CLINIT_SMALI = r'''
const/16 v0, {}
new-array v0, v0, [Z
sput-object v0, Ltool/acv/AcvReporter;->{}:[Z
'''

    REPORTER_SMALI = r'''.class public final Ltool/acv/AcvReporter;
.super Ljava/lang/Object;

# static fields
{fields}

# direct methods
.method static constructor <clinit>()V
    .locals 1
    {field_inits}
    return-void
.end method

.method private constructor <init>()V
    .locals 1

    invoke-direct {{p0}}, Ljava/lang/Object;-><init>()V

    return-void
.end method

'''

    SAVE_EXTERNAL_FILE_SMALI = r'''
.method public static saveExternalPublicFile(Ljava/io/File;)V
    .locals 6
    .param p0, "file"    # Ljava/io/File;

    .prologue
    const/4 v4, 0x1

    const/4 v3, 0x0

    .line 31
    invoke-virtual {{p0, v4, v3}}, Ljava/io/File;->setReadable(ZZ)Z

    .line 35
    :try_start_0
    new-instance v2, Ljava/io/FileOutputStream;

    invoke-direct {{v2, p0}}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    .line 36
    const/16 v3, {number} # number of smali/class files 

    new-array v0, v3, [[Z

    #.line 37
    .local v0, "array":[[Z
    
    #start of array adding
    
    {arrays}
    
    #end of array adding

    invoke-static {{v2, v0}}, Ltool/acv/AcvReporter;->saveBooleanArrayToFile(Ljava/io/FileOutputStream;[[Z)V

    invoke-virtual {{v2}}, Ljava/io/FileOutputStream;->flush()V

    invoke-virtual {{v2}}, Ljava/io/FileOutputStream;->close()V
    :try_end_0
    .catch Ljava/io/IOException; {{:try_start_0 .. :try_end_0}} :catch_0

    .end local v0    # "array":[[Z
    :goto_0
    return-void

    :catch_0
    move-exception v1

    .local v1, "e":Ljava/io/IOException;
    invoke-virtual {{v1}}, Ljava/io/IOException;->printStackTrace()V

    const-string v3, "AcvInstrumentation"

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {{v4}}, Ljava/lang/StringBuilder;-><init>()V

    const-string v5, ":reporter: "

    invoke-virtual {{v4, v5}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {{v1}}, Ljava/io/IOException;->getMessage()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {{v4, v5}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {{v4}}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {{v3, v4}}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_0
.end method

.method public static saveBooleanArrayToFile(Ljava/io/FileOutputStream;[[Z)V
    .locals 8
    .param p0, "fs"    # Ljava/io/FileOutputStream;
    .param p1, "array"    # [[Z
    .annotation system Ldalvik/annotation/Throws;
        value = {{
            Ljava/io/IOException;
        }}
    .end annotation

    .line 28
    array-length v0, p1

    const/4 v1, 0x0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v0, :cond_2

    aget-object v3, p1, v2

    .line 29
    .local v3, "subarray":[Z
    array-length v4, v3

    const/4 v5, 0x0

    :goto_1
    if-ge v5, v4, :cond_1

    aget-boolean v6, v3, v5

    .line 30
    .local v6, "elem":Z
    if-eqz v6, :cond_0

    const/16 v7, 0x31

    goto :goto_2

    :cond_0
    const/16 v7, 0x30

    :goto_2
    invoke-virtual {{p0, v7}}, Ljava/io/FileOutputStream;->write(I)V

    .line 29
    .end local v6    # "elem":Z
    add-int/lit8 v5, v5, 0x1

    goto :goto_1

    .line 32
    :cond_1
    const/16 v4, 0xa

    invoke-virtual {{p0, v4}}, Ljava/io/FileOutputStream;->write(I)V

    .line 28
    .end local v3    # "subarray":[Z
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 34
    :cond_2
    return-void
.end method
'''
