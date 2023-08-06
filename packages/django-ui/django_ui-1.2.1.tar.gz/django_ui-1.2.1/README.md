# Django UI 

Dynamic fields and settings theme color admin

**Conditional fields show/hidden**

- Show or hidden fields
- Changed color theme admin app
- Preview of images in forms


###### Version Python: `^3`
###### Version django: `^2.2`

## Installation
- `pip install django_ui`
- Add of first `django_ui` to your installed apps
- Run migrations `./ manage.py migrations`


## Usage (Show or hidden fields)

**Conditional choice**
- Add the class `{name_choice} j__{key_choice}` to the trigger element

**Conditional Checkbox**
- Add the class `j__{name_bolean}` to the trigger element


To use, create the forms.py file and add the class created in ModelAdmin

#### Example choice: `{name_choice} j__{key_choice}`

forms.py

```python
from django import forms

class ModelExampleForm(forms.ModelForm):
    occupation = forms.ChoiceField(choices=[
            ('study', 'Study'),
            ('work', 'Work')
        ], )
    study = forms.CharField(label='Name Institution', required=False,
                            widget=forms.TextInput(attrs={'class': "occupation j__study"}))
    semester = forms.CharField(label='Semester', required=False,
                               widget=forms.TextInput(attrs={'class': "occupation j__study"}))
    company = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'class': "occupation j__work"}))
    position = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': "occupation j__work"}))
```


admin.py

```python
from django.contrib import admin

from your_app.forms import ModelExampleForm
from your_app.models import ModelExample

class ModelExampleAdmin(admin.ModelAdmin):
    model = ModelExample
    form = ModelExampleForm
``` 

\
### Example checkbox:  `j__{name_bolean}`

```python
from django import forms

class ModelExampleForm(forms.ModelForm):
    ...
    nick = forms.BooleanField(required=False, label='Add NickName?', help_text='Select if you want to add NickName',
                                  widget=forms.CheckboxInput())
    nickname = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "j__nick"}))

```
\
**NOTE:** In the form just add the fields you want to be dynamic


\
Preview

![Screenshot](./media/django_ui.gif)


## Usage (Show or hidden fields)

- Create as many themes as you want and activate the one you want
![Screenshot](./media/theme_ui.gif)


## Example of image file

- Preview of images in forms

![Screenshot](./media/django_images.png)



By default app hidden:

- Show model example: 
   
    In settings create var `DJANGO_UI_SHOW_MODEL_EXAMPLE_DYNAMIC = True`
   
   
   
- Use model theme:

    In settings create var `USE_APP_THEME_UI_ADMIN = True`   




Made with ♥ by [Jose Florez](www.joseflorez.co)