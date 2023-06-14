from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.toast import toast
import re
import os
from google.cloud import bigquery
# import mysql.connector
import pandas as pd
class SignupScreen(MDScreen):
    Builder.load_file("signup.kv")
    def signup(self):
        fname=self.ids['fname'].text
        lname = self.ids['lname'].text
        email=self.ids['email'].text
        password=self.ids['password'].text
        email_pattern="['a-zA-Z0-9']+@[a-zA-Z]+\.[com|edu|ng|org]"


        if fname==""  or lname=="" or email=="" or password=='':
            toast("All fields must be filled")
        elif fname.isalpha() is False:
            toast(' name can only contain alphabets')
        elif lname.isalpha() is False:
            toast(' name can only contain alphabets')

        elif not re.search(email_pattern,email):
            toast("incorrect email")

        elif len(password) >16:
            toast("password should be 16 character long")


        else:
            # Set up the BigQuery client and table reference
            try:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cloud_key.json'
                project_id = 'my-project-356323'
                dataset_id = 'emaildb'
                client = bigquery.Client()

                table_id = 'user_data'  # this table already exists in bigquery
                table_ref = client.dataset(dataset_id).table(table_id)
                table = bigquery.Table(table_ref)
                df1 = pd.DataFrame({'firstname': [fname], 'latname': [lname], 'email': [email], 'password': [password]})

                # to append data
                job_config = bigquery.LoadJobConfig(

                    write_disposition="WRITE_APPEND"
                )

                job = client.load_table_from_dataframe(df1, table_ref, location='US', job_config=job_config)

                # Wait for the load job to complete
                job.result()
                toast('Sign Up successful')
            except Exception as e:
                print(str(e))
