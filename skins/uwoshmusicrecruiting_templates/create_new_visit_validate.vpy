#if not context.REQUEST.get('school_title') and not context.REQUEST.get('schools_drop_down'):
#    state.setError('school_title', 'You must either enter a new school or select an existing one!', new_status='failure')
    
#if not context.REQUEST.get('student_title') and not context.REQUEST.get('students_drop_down'):
#    state.setError('student_title', 'You must either enter a new student name or select an exisiting one!', new_status='failure')
    
#if not context.REQUEST.get('contact_title') and not context.REQUEST.get('contacts_drop_down'):
#    state.setError('contact_title', 'You must either enter a new contact or select an existing one!', new_status='failure')
    

if context.REQUEST.get('school_title') and context.REQUEST.get('schools_drop_down'):
    state.setError('school_title', 'You must select an existing student or create a new one.  You can\'t do both!', new_status='failure')
    
if context.REQUEST.get('student_title') and context.REQUEST.get('students_drop_down'):
    state.setError('student_title', 'You must select an existing student or create a new one.  You can\'t do both!', new_status='failure')
    
if context.REQUEST.get('contact_title') and context.REQUEST.get('contacts_drop_down'):
    state.setError('contact_title', 'You must select an existing contact or create a new one.  You can\'t do both!', new_status='failure')
    
if len(context.REQUEST.get('facultymember_title')) is 0 and len(context.REQUEST.get('facultymembers_drop_down')) is 0:
    state.setError('facultymember_title', 'You must either choose a fuculty or enter a new one!', new_status='failure')
    
faculty_dd_id = context.REQUEST.get('facultymembers_drop_down')
faculty_field_id = context.REQUEST.get('facultymember_title')
user_id = context.portal_membership.getAuthenticatedMember().id

    
return state