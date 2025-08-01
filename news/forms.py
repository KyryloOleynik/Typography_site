from django import forms
from .models import News
import re

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

    def clean_content(self):
        content = self.cleaned_data.get('content')

        pattern = r'(<oembed url="https://www\.youtube\.com/watch\?v=([^"]+)"></oembed>)'

        def replacer(match):
            oembed_tag = match.group(1)
            video_id = match.group(2)
            iframe = f'<iframe width="100%" height="600" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
            return f'{oembed_tag}\n{iframe}'

        if content:
            content = re.sub(pattern, replacer, content)

        return content