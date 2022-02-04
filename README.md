# Grupo Microanalisis Budget Tool Prototype
#### This tool is currently not live; however, repo was made pubilc as a way to display my project with some information removed
### Will not run unless provided oracle client and oracle database credentials. All required pip packages are in the requirements.txt and can be install with the following command:
```
pip install pipenv
pipenv install
````

<img src="https://github.com/raulescobar-g/manalisis_webapp_prototype/blob/main/website/static/logi.png?raw=true" width=300/>
<img src="https://github.com/raulescobar-g/manalisis_webapp_prototype/blob/main/website/static/acct.png?raw=true" width=300 />
<img src="https://github.com/raulescobar-g/manalisis_webapp_prototype/blob/main/website/static/idx.png?raw=true" width=300 />


 - ## Routes
    #### Unprotected
    - /
    - /acct_creation
    #### Protected
    - /user
    - /project_view
    - /project_selection
        - /budget/<int: project_id>
        - /table/<int: project_id>
        - /table/show_img
        - /table/show_xml
        - /table/delete/<int: project_id>
    - /xml_upload
    - /xml_success
    - /logout
    - /email_confirm/<token>

- ## Models
    - User 
        - Project Orders
            - Receipts
            - XML files

#### for more info contact me at raulescobar_g@tamu.edu







