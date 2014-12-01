from Products.PythonScripts.standard import url_quote, urlencode

def get_folder(t, name):
    folder_queried = context.queryCatalog({'portal_type':t, 'title':name})[0]
    return folder_queried.getObject()

def create_object_in_directory(container, t):
    id = container.generateUniqueId(t)
    container.invokeFactory(id=id, type_name=t)
    return container[id]

def create_with_id_object_in_directory(container, t, id):
    container.invokeFactory(id=id, type_name=t)
    return container[id]

def set_reference(object, visit):
    existing_visits = object.getVisits()

    if visit not in existing_visits:
        existing_visits.append(visit)
        object.setVisits(existing_visits)

#create visit
visit_id = context.REQUEST.get('id')
new_visit = None
is_new_visit = True

#check if id has already been generated
if visit_id:
    #check if it is just editing existing visit
    old_visits = context.queryCatalog({'portal_type':'Visit', 'id':visit_id})
    if len(old_visits) is 0:
        new_visit = create_with_id_object_in_directory(get_folder('VisitFolder', 'Visits'), 'Visit', visit_id)
    else:
        new_visit = old_visits[0].getObject()
        is_new_visit = False
else:
    new_visit = create_object_in_directory(get_folder('VisitFolder', 'Visits'), 'Visit')


#Create School and add to Visit object
if context.REQUEST.get('school_title'):
    
    new_school = create_object_in_directory(get_folder('SchoolFolder', 'Schools'), 'School')
    
    new_school.edit(title=context.REQUEST.get('school_title'))
    new_visit.edit(title=new_school.Title().replace(' ', ''), schools = new_school)
    
    set_reference(new_school, new_visit)
    
elif len(context.REQUEST.get('schools_drop_down')) > 0:
    existing_school = get_folder('SchoolFolder', 'Schools')[context.REQUEST.get('schools_drop_down')]
    set_reference(existing_school, new_visit)
    new_visit.edit(title=existing_school.Title().replace(' ', ''), schools=existing_school)


#Create Student and add to Visit Object
if context.REQUEST.get('student_title'):

    new_student = create_object_in_directory(get_folder('StudentFolder', 'Students'), 'Student')

    is_committed = False
    if context.REQUEST.get('isCommittedToAttend'):
        is_committed = True

    new_student.edit(title = context.REQUEST.get('student_title'), \
             phone = context.REQUEST.get('student_phone'), \
             email = context.REQUEST.get('student_email'), \
             instrument = context.REQUEST.get('student_instrument'), \
             address = context.REQUEST.get('student_address'), \
             city = context.REQUEST.get('student_city'), \
             state = context.REQUEST.get('student_state'), \
             zip = context.REQUEST.get('student_zip'), \
             isCommittedToAttend = is_committed)
             
    set_reference(new_student, new_visit)

    new_visit.edit(title = new_visit.Title() + '-' + new_student.Title().replace(' ', ''), students = new_student)

elif len(context.REQUEST.get('students_drop_down')) > 0:
    existing_student = get_folder('StudentFolder', 'Students')[context.REQUEST.get('students_drop_down')]
    
    set_reference(existing_student, new_visit)
    
    name = new_visit.Title() + '-' + existing_student.Title().replace(' ', '')
    new_visit.edit(title = name, students = existing_student)


#Create Contact and add to Visit  
if context.REQUEST.get('contact_title'):

    new_contact = create_object_in_directory(get_folder('ContactFolder', 'Contacts'), 'Contact')

    is_alumni = False
    if context.REQUEST.get('contact_isAlumni'):
        is_alumni = True
    
    new_contact.edit(title = context.REQUEST.get('contact_title'), \
             type = context.REQUEST.get('contact_type'), \
             phone = context.REQUEST.get('contact_phone'), \
             email = context.REQUEST.get('contact_email'), \
             address = context.REQUEST.get('contact_address'), \
             city = context.REQUEST.get('contact_city'), \
             state = context.REQUEST.get('contact_state'), \
             zip = context.REQUEST.get('contact_zip'), \
             isAlumni = is_alumni)
             
    set_reference(new_contact, new_visit)
    
    name = new_visit.Title() + '-' + new_contact.Title().replace(' ', '')
    new_visit.edit(title = name, contacts = new_contact)
    
elif len(context.REQUEST.get('contacts_drop_down')) > 0:

    existing_contact = get_folder('ContactFolder', 'Contacts')[context.REQUEST.get('contacts_drop_down')]

    set_reference(existing_contact, new_visit)

    name = new_visit.Title() + '-' + existing_contact.Title().replace(' ', '')
    new_visit.edit(title = name, contacts = existing_contact)
    
    
faculty_dd_id = context.REQUEST.get('facultymembers_drop_down')
faculty_field_id = context.REQUEST.get('facultymember_title')
user_id = context.portal_membership.getAuthenticatedMember().id

#Create Faculty and add to visit
if faculty_dd_id is faculty_field_id:
    existing_faculty = get_folder('FacultyMemberFolder', 'FacultyMembers')[faculty_dd_id]

    set_reference(existing_faculty, new_visit)

    name = new_visit.Title() + '-' + existing_faculty.getName()
    new_visit.edit(title = name, facultymembers = existing_faculty)

elif  len(faculty_dd_id) > 0:
    existing_faculty = context.queryCatalog({'portal_type':'FacultyMember', 'id':faculty_dd_id})
    faculty = None
    
    if len(existing_faculty) > 0:
        faculty = existing_faculty[0]
        faculty = faculty.getObject()
            
        set_reference(faculty, new_visit)
    else:
        faculty  = create_object_in_directory(get_folder('FacultyMemberFolder', 'FacultyMembers'), 'FacultyMember')
        faculty.edit(title = context.REQUEST.get('faculty_dd_id'))
        
        set_reference(faculty, new_visit)

    new_visit.edit(title = new_visit.Title() + '-' + faculty.Title(), facultymembers = faculty)

else:
    existing_faculty = context.queryCatalog({'portal_type':'FacultyMember', 'Title':faculty_field_id})
    faculty = None

    if len(existing_faculty) > 0:
        faculty = existing_faculty[0]
        faculty = faculty.getObject()
    
        if faculty.getEmail() != context.REQUEST.get('facultymember_email'):
            faculty.edit(email = context.REQUEST.get('facultymember_email'))
            
        set_reference(faculty, new_visit)

    else:
        faculty  = create_object_in_directory(get_folder('FacultyMemberFolder', 'FacultyMembers'), 'FacultyMember')
        faculty.edit(title = context.REQUEST.get('facultymember_title'), email = context.REQUEST.get('facultymember_email'))

        set_reference(faculty, new_visit)

    new_visit.edit(title = new_visit.Title() + '-' + faculty.Title(), facultymembers = faculty)


#get date and notes
date = context.REQUEST.get('dateOfVisit_year') + '/' + \
     context.REQUEST.get('dateOfVisit_month') + '/' + \
     context.REQUEST.get('dateOfVisit_day') + ' ' + \
     context.REQUEST.get('dateOfVisit_hour') + ':' + \
     context.REQUEST.get('dateOfVisit_minute') + ' ' + \
     context.REQUEST.get('dateOfVisit_ampm')
new_visit.edit(notes = context.REQUEST.get('notes'), dateOfVisit = date)

link = context.portal_url.getPortalObject().absolute_url() + '/' + \
     get_folder('VisitFolder', 'Visits').id + '/' + new_visit.id

state.setNextAction ('redirect_to:string:' + link)


instrument = None
student_name = None

if context.REQUEST.get('student_title'):
    instrument = context.REQUEST.get('student_instrument')
    student_name = context.REQUEST.get('student_title')
else:
    existing_contact = get_folder('StudentFolder', 'Students')[context.REQUEST.get('students_drop_down')]
    instrument = existing_contact.getInstrument()
    student_name = existing_student.Title()
    
    
#email professors who have the selected instrument in their preferences
if instrument and student_name and is_new_visit:
    school_name = None
    if context.REQUEST.get('school_title'):
        school_name = context.REQUEST.get('school_title')
    else:
        school_name = get_folder('SchoolFolder', 'Schools')[context.REQUEST.get('schools_drop_down')].Title()
    
    context.mail_by_instrument_type(instrument, student_name, school_name, link)

    
return state