from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Book, Chapter, Rating, Comment, BookmarkList


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        label='Я регистрируюсь как',
        widget=forms.RadioSelect,
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()
        return user


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'genre', 'cover', 'audio']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 15}),
        }


class TxtUploadForm(forms.Form):
    txt_file = forms.FileField(
        label='Файл .txt или .docx (разбивается на главы)',
        help_text='Главы ищутся по строкам «Глава 1», «Глава 2»… или «# …»',
    )

    def clean_txt_file(self):
        f = self.cleaned_data['txt_file']
        name = f.name.lower()
        if not (name.endswith('.txt') or name.endswith('.docx')):
            raise forms.ValidationError('Нужен файл .txt или .docx')
        if f.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Файл больше 5 МБ')
        if name.endswith('.docx'):
            import io
            import zipfile
            try:
                with zipfile.ZipFile(io.BytesIO(f.read())) as zf:
                    if 'word/document.xml' not in zf.namelist():
                        raise forms.ValidationError('Похоже, это не документ Word')
            except zipfile.BadZipFile:
                raise forms.ValidationError('Файл повреждён или не .docx')
            f.seek(0)
        return f


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect,
        }
        labels = {'value': 'Оценка'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий...'}),
        }
        labels = {'text': ''}


class BookmarkListForm(forms.ModelForm):
    class Meta:
        model = BookmarkList
        fields = ['name']
        labels = {'name': 'Название списка'}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Например: Любимое'}),
        }
