from django import forms

categories = [('No category', 'No category'), ('Furniture', 'Furniture'), ('Sports', 'Sports'), ('Home decor', 'Home Decor'),
    ('Arts', 'Arts'), ('Jewelry', 'Jewelry'), ('Books', 'Books'), ('Electronics', 'Electronics'),
    ('Exercise', 'Exercise'), ('Other', 'Other')]

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title')
    starting_bid = forms.IntegerField(label='Starting Bid')
    image_url = forms.URLField(label='Image URL', required=False, max_length=300)
    category = forms.CharField(label='Category', widget=forms.Select(choices=categories), required=False)
