# from django.db import models
# from django.urls import reverse

# class Game(models.Model):
#     title = models.CharField(verbose_name='TITLE', max_length=50)
#     slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.')
#     description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
#     content = models.TextField('CONTENT')
#     create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
#     modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

#     class Meta:
#         verbose_name = 'game' #테이블 단수 별칭
#         verbose_name_plural = 'games' #테이블 복수 별칭
#         db_table = 'blog_games' #디폴트는 앱명_모델명
#         ordering = ('-modify_dt',) #출력 시 modify_dt를 기준으로 내림차순 정렬
    
#     def __str__(self):
#         return self.title
    
#     def get_absolute_url(self):
#         return reverse('blog:game_detail', args=(self.slug,))
    
#     def get_previous(self):
#         return self.get_previous_by_modify_dt()#장고의 내장함수, modify_dt()를 기준으로 최신포스트를 반환

#     def get_next(self):
#         return self.get_next_by_modify_dt()