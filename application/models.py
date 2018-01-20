from __future__ import unicode_literals
from django.db import models

class category(models.Model):
    name = models.CharField(max_length=200)
    feature = models.BooleanField()
    activeyn = models.BooleanField()
    type = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str({
            "name": str(self.name), 
            "feature": str(self.feature), 
            "type": str(self.type),
            "activeyn": str(self.activeyn)
            })


class artist(models.Model):
    name = models.CharField(max_length=500)
    cover_image = models.TextField(default=None)
    activeyn = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str({
            "name": str(self.name),
            "cover_url": str(self.cover_image),
            "activeyn": str(self.activeyn)
            })

class video(models.Model):
    name = models.CharField(max_length=500)
    cover_image = models.TextField()
    mpd_url = models.TextField()
    mp4_url = models.TextField()
    category = models.ManyToManyField(category)
    m_order = models.IntegerField(default=0)
    activeyn = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str({
            'name': str(self.name),
            'm_order': str(self.m_order),
            'activeyn': self.activeyn
            })
    
    @classmethod
    def add_category(cls, video, category_id):
        video, created = cls.objects.get_or_create(id=video.id)
        video.category.add(category_id)

    @classmethod
    def remove_category(cls, video, category_id):
        video, created = cls.objects.get_or_create(id=video.id)
        video.category.remove(category_id)

class track(models.Model):
    name = models.CharField(max_length=500)
    cover_image = models.TextField()
    mp3_url = models.TextField()
    video = models.ManyToManyField(video)
    category = models.ManyToManyField(category)
    m_order = models.IntegerField(default=0)
    activeyn = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str({
            'name': str(self.name),
            'mp3_url': str(self.mp3_url),
            'm_order': str(self.m_order),
            'activeyn': self.activeyn
            })
    
    @classmethod
    def add_category(cls, track, category_id):
        track, created = cls.objects.get_or_create(id=track.id)
        track.category.add(category_id)

    @classmethod
    def remove_category(cls, track, category_id):
        track, created = cls.objects.get_or_create(id=track.id)
        track.category.remove(category_id)

    @classmethod
    def add_video(cls, track, video_id):
        track, created = cls.objects.get_or_create(id=track.id)
        track.video.add(video_id)

    @classmethod
    def remove_video(cls, track, video_id):
        track, created = cls.objects.get_or_create(id=track.id)
        track.video.remove(video_id)

class album(models.Model):
    name = models.CharField(max_length=500)
    release_date = models.DateTimeField(auto_now=True)
    cover_image = models.TextField()
    category = models.ManyToManyField(category)
    artist = models.ManyToManyField(artist)
    tracks = models.ManyToManyField(track)
    video = models.ManyToManyField(video)
    m_order = models.IntegerField(default=0)
    activeyn = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str({
            'name': str(self.name),
            'release_date': str(self.release_date.strftime("%Y-%m-%d")),
            'cover_url': str(self.cover_image),
            'm_order': str(self.m_order),
            'activeyn': self.activeyn
            })

    @classmethod
    def add_category(cls, album, category_id):
        album, created = cls.objects.get_or_create(id=album.id)
        album.category.add(category_id)

    @classmethod
    def remove_category(cls, album, category_id):
        album, created = cls.objects.get_or_create(id=album.id)
        album.category.remove(category_id)
    
    @classmethod
    def add_artist(cls, album, artist_id):
        album, created = cls.objects.get_or_create(id=album.id)
        album.artist.add(artist_id)

    @classmethod
    def remove_artist(cls, album, artist_id):
        album, created = cls.objects.get_or_create(id=album.id)
        album.artist.remove(artist_id)

    @classmethod
    def add_track(cls, album_id, track_id):
        album, created = cls.objects.get_or_create(id=album_id)
        album.tracks.add(track_id)

    @classmethod
    def remove_track(cls, album_id, track_id):
        album, created = cls.objects.get_or_create(id=album_id)
        album.tracks.remove(track_id)

    @classmethod
    def add_video(cls, album, video_id):
        album, created = cls.objects.get_or_create(id=album.id)
        album.video.add(video_id)

    @classmethod
    def remove_video(cls, album, video_id):
        album, created = cls.objects.get_or_create(id=album.id)
        album.video.remove(video_id)