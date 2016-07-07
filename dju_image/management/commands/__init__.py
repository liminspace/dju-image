def profiles_validate(profiles):
    from ... import settings as dju_settings
    if profiles is None:
        return
    allow_profiles = set(tuple(dju_settings.DJU_IMG_UPLOAD_PROFILES.keys()) + ('default',))
    for profile in profiles:
        if profile not in allow_profiles:
            return 'Profile "{}" does not exist in settings.DJU_IMG_UPLOAD_PROFILES.'.format(profile)
