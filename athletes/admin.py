from django.contrib import admin
from .models import Profile, Achievement, Stat, Video

# Register your models here.
# @admin.register(Athlete)
# class AthleteAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'age', 'sport', 'organization')
#     search_fields = ('first_name', 'last_name', 'organization__name') # Search by Org name too!
#     list_filter = ('sport', 'organization')
#     ordering = ('last_name', 'first_name')
    
#     # Optional: Makes the organization dropdown easier to use if you have many orgs
#     autocomplete_fields = ['organization']

class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1  # Number of empty rows to show by default
    fields = ('emoji', 'achievement')

class StatInline(admin.TabularInline):
    model = Stat
    extra = 1  # Number of empty rows to show by default
    fields = ('date', 'event', 'performance', 'highlight')

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1  # Number of empty rows to show by default
    fields = ('url',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [AchievementInline, StatInline, VideoInline]
    list_display = ('first_name', 'last_name', 'organization', 'sport')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # 1. Superusers see everything
        if request.user.is_superuser:
            return qs

        # 2. Organization/School Admins see only their own athletes
        # We check if the user 'owns' an organization
        if hasattr(request.user, 'organization'):
            return qs.filter(organization=request.user.organization)
        
        # 3. Athletes see only themselves
        if hasattr(request.user, 'athlete'):
            return qs.filter(user=request.user)
        
        # Fallback: See nothing
        return qs.none()

    def get_readonly_fields(self, request, obj=None):
        """
        Prevent Athletes from editing sensitive fields inherited from Athlete.
        """
        # If the user is an athlete (and not a superuser), lock these fields
        if not request.user.is_superuser and hasattr(request.user, 'athlete'):
            return ['organization', 'sport', 'user'] # Also lock 'user' link
        return []

    def has_add_permission(self, request):
        """
        Athletes cannot create NEW profiles. Only Orgs and Superusers can.
        """
        if hasattr(request.user, 'athlete'):
            return False
        return True

    # Ensure they can only add achievements to their own profile
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Achievement):
                # If they aren't superuser, force the profile to be theirs
                if not request.user.is_superuser:
                    instance.profile = request.user.athlete.profile 
            elif isinstance(instance, Stat):
                # If they aren't superuser, force the profile to be theirs
                if not request.user.is_superuser:
                    instance.profile = request.user.athlete.profile 
            elif isinstance(instance, Video):
                # If they aren't superuser, force the profile to be theirs
                if not request.user.is_superuser:
                    instance.profile = request.user.athlete.profile 
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        """
        Auto-link the profile to the organization if created by an Org Admin.
        """
        # Note: 'organization' is a field inherited from the Athlete parent
        if not request.user.is_superuser and hasattr(request.user, 'organization'):
            obj.organization = request.user.organization
        
        super().save_model(request, obj, form, change)

# @admin.register(Athlete)
# class AthleteAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'organization', 'sport')
    
#     def get_queryset(self, request):
#         """
#         Filter the list of athletes based on the logged-in user.
#         """
#         qs = super().get_queryset(request)
        
#         # 1. Superusers see everything
#         if request.user.is_superuser:
#             return qs
        
#         # 2. Organization/School Admins see only their own athletes
#         # We check if the user 'owns' an organization
#         if hasattr(request.user, 'organization'):
#             return qs.filter(organization=request.user.organization)
            
#         # 3. Athletes see only themselves
#         if hasattr(request.user, 'athlete'):
#             return qs.filter(user=request.user)
            
#         # Fallback: See nothing
#         return qs.none()

#     def get_readonly_fields(self, request, obj=None):
#         """
#         Prevent Athletes from editing sensitive fields (like their Organization).
#         """
#         if not request.user.is_superuser and hasattr(request.user, 'athlete'):
#             return ['organization', 'sport'] # Lock these fields for athletes
#         return []

#     def save_model(self, request, obj, form, change):
#         """
#         When an Organization creates an athlete, automatically link it 
#         to that Organization.
#         """
#         # If the user is an Org Admin and creating a new athlete
#         if not request.user.is_superuser and hasattr(request.user, 'organization'):
#             obj.organization = request.user.organization
        
#         super().save_model(request, obj, form, change)

#     def has_add_permission(self, request):
#         """
#         Athletes cannot create NEW athlete profiles. 
#         Only Orgs and Superusers can.
#         """
#         if hasattr(request.user, 'athlete'):
#             return False
#         return True