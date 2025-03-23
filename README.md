# Endometrial Cancer Tool (Demo)
## Projects Aim

The Endometrial Cancer Tool (Demo) is a cutting-edge web application designed to statistically analyze this disease survival and generate comprehensive survival plots.

It simplifies the complex process of survival analysis, to easily create statistic plots with no need of previous bioinformatic or statistics knowledge.

## Technologies and libraries

- Python 3.10.12
- Django 4.2.20
- Dash 2.18.2
- Dash Bio 1.0.2
- Plotly 5.20.0
- Pandas 2.1.4
- Scikit.
- Lifelines 0.27.7
- HTML.
- CSS.
- Bootstrap.
- jQuery/jQuery-UI

## Project

1. ### Directory structure.
	All the project directories are named and explained in the next list. At the end of the list there is a structure tree image:
	- **<font size=4>ect_demo</font>**: This is the <span style="color: green;">**main folder**</span> that contains the <span style='color: lightgreen;'>**ect_demo**</span> project, and the **requirements.txt** file.

		- **<font size=4><span style='color: lightgreen;'>ect_demo</span></font>**: This is the project folder that contains the <span style='color: steelblue;'>**ect_demo**</span> and the <span style='color: lightblue;'>**ect_tool**</span> folders, and the <span style='color: gold;'>**survival.csv**</span> dataset file.

			- **<font size=3><span style='color: steelblue;'>**ect_demo:**</span></font>** Contains all the settings for the Django project.
			- **<font size=3><span style='color: lightblue;'>**ect_tool:**</span></font>** The Django app called **Endometrial Cancer Tool (Demo)**. Contains all the front-end and back-end code for the Endometrial Cancer Tool (Demo), following the Django project structure specifications.

				- **<font size=3>migrations:</font>** ECT (Demo) model migrations.
				- **<font size=3>static/ect_tool:</font>** Contains all the files for styling and event management for **ECT (Demo)**. CSS, images, JavaScript and Bootstrap files.
					- **css**: All CSS files for ECT (Demo) style.
					- **img**: Predefined images for ECT (Demo) views.
					- **vendor**: Folder containing Bootstrap, jQuery and jQuery-UI files.
				- **<font size=3>templates/ect_tool:</font>** Contains all the HTML templates for the ECT (Demo).
			- **<font size=3><span style='color: gold;'>**survival.csv:**</span></font>** Dataset as a CSV file contianing all the Endometrial Cancer data needed for the application.
			
		
	- <font size=4>**Directory tree structure**</font>:

 	 	![Directory structure](https://github.com/XLlobet/ect_demo/blob/main/ect_demo%20tree.png)

2. ### Location of the main function.
      The main door or function of the project, is the ***ìndex()*** function from **views.py** file from ***'ect_demo/ect_demo/ect_tool'*** folder. 

3. ### How run the application.
   
   	Install the packages needed using the **requirements.txt** file.
   
	```bash
	pip install -r requirements.txt
	```

	Clone the repository.

	```bash
	git clone https://github.com/XLlobet/ect_demo.git
	cd ect_demo/ect_demo
	```

	Run the application:

	```bash
	python3 manage.py migrate
	python3 manage.py runserver
	```

  	 Visite the app in your brouser at ***http://127.0.0.1:8000/***

