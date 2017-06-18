# BIMM-185-Final-Report

#Tiffany Gassmann
#BIMM 185 Final Project

#Using Serum as a Diagnostic Tool for Multiple Sclerosis

#Process Relationship file - cotains info regarding the patients disease status, age, sex
#Create output to load into MySQL

def process_relationship_file():
    rel_open = open("Data_rel")
    rel_read = rel_open.readlines()

    #dictionary that uses patient_id as key and value is a list containing status,age,sex
    patients = {}

    #data_rel file patient by patient
    for line in rel_read:
        entry = line.split('\t')

        #Extracted info for each patient
        source_name = entry[0]
        disease_state = entry[2]
        age = entry[4]
        sex = entry[10]

        #list to store status,age, sex - used for each key,value in dictionary
        patient_entry = [disease_state,age,sex]
        patients[source_name] = patient_entry

        #output for MySql Patient_info table
        #print "\t".join([source_name, disease_state, age, sex])


    #Returns Dictionary mapping patient_id to status,age,sex
    return patients


#Processes MicroArray Text Files - contains info regarding the different mRNAs as well as
# their corresponding p-values and detection status - the detection "True" or "False" values
# are based on their log2 intensity signal after normalization and summarization

def process_microarray_file(patients_dict):
    #Loaded with Arrays of Tuples containing the different fields for each mRNA
    healthy_sorted = []
    relapse_sorted = []
    remission_sorted = []

    #open each microarray file
    for key,value in patients_dict.items():
            file_name = "{}_sample_table.txt".format(key)
            micro_open = open(file_name)
            micro_read = micro_open.readlines()[1:]

            #Access the array key for each patient_id
            status = str(value[0])
            age = value[1]
            sex = value[2]

            #iterate over each mRNA
            for line in micro_read:
                entry = line.split('\t')
                mRNA_id_ref = entry[0]
                #print mRNA_id_ref
                value = entry[1]
                detection_p_val = entry[2]
                detection = entry[3]

                #Sorting each file based on the Status mapped from the dictionary
                if status == "Healthy control" and detection == "True\n":
                    healthy_sorted.append((mRNA_id_ref,detection_p_val,age,sex))

                if status == "MS relapse" and detection == "True\n":
                    relapse_sorted.append((mRNA_id_ref,detection_p_val,age,sex))

                if status == "MS remission" and detection == "True\n":
                    remission_sorted.append((mRNA_id_ref,detection_p_val,age,sex))
    #Sort by p-value
    healthy_sorted.sort(key=lambda x: x[1])
    relapse_sorted.sort(key=lambda x: x[1])
    remission_sorted.sort(key=lambda x: x[1])


    #print "RNA's found in Healthy: ",len(healthy_sorted)," RNA's Found in Relapsed: ", len(relapse_sorted),
    #  " RNA's found in Remission: ",len(remission_sorted)
    with open("Healthy Control RNA's", "w") as fp:
          fp.write('\n'.join('%s \t %s \t %s \t %s' % x for x in healthy_sorted))
    with open("MS Remission RNA's", "w") as fp:
          fp.write('\n'.join('%s \t %s \t %s \t %s' % x for x in remission_sorted))
    with open("MS Relapse RNA's", "w") as fp:
        fp.write('\n'.join('%s \t %s \t %s \t %s' % x for x in relapse_sorted))

    for mRNA in healthy_sorted:
        print '\t'.join([str(i) for i in mRNA])

patients_dict = process_relationship_file()
process_microarray_file(patients_dict)


process_relationship_file()

