import csv, os
from Products.CMFCore.utils import getToolByName

def get_folder(self, type, name):
    folder_brains = self.queryCatalog({'portal_type':type, 'title':name})[0]
    return folder_brains.getObject()

def create_object_in_directory(self, container, type):
    id = container.generateUniqueId(type)
    container.invokeFactory(id=id, type_name=type)
    return container[id]

def get_type_or_create(self, type, folder, cmp, val):
    brains = self.queryCatalog({'portal_type':type, cmp:val})
    if len(brains) > 0:
        return brains[0].getObject()
    else:
        return create_object_in_directory(self, folder, type)

def set_reference(self, object, visit):
    existing_visits = object.getVisits()

    if visit not in existing_visits:
        existing_visits.append(visit)
        object.setVisits(existing_visits)

def import_visits(self):
    reader = csv.reader(self.REQUEST.get('csv-file-contents').split(os.linesep), delimiter="\t")

    for row in reader:
        if not row: continue

        header = ['School', 'Student Name', 'Instrument', 'Student Email', 'Student Phone', 'Student Address', 'Student City',
            'Student Zip', 'Contact Name', 'Contact Title', 'Contact Phone', 'Contact Email', 'Is Contact Alumni', 'Date']
    
        school_name = row[0].strip().strip('"').strip("'")
        student_name = row[1].strip().strip('"').strip("'")
        instrument = row[2].strip().strip('"').strip("'")
        student_email = row[3].strip().strip('"').strip("'")
        student_phone = row[4].strip().strip('"').strip("'")
        student_address = row[5].strip().strip('"').strip("'")
        student_city = row[6].strip().strip('"').strip("'")
        student_zip = row[7].strip().strip('"').strip("'")
        contact_name = row[8].strip().strip('"').strip("'")
        contact_title = row[9].strip().strip('"').strip("'")
        contact_phone = row[10].strip().strip('"').strip("'")
        contact_email = row[11].strip().strip('"').strip("'")
        is_contact_alumni = row[12].strip().upper() == 'TRUE'
        date = row[13].strip().strip('"').strip("'")

        user_id = self.portal_membership.getAuthenticatedMember().id
        
        student = get_type_or_create(self, 'Student', get_folder(self, 'StudentFolder', 'Students'), 'title', student_name)
        contact = get_type_or_create(self, 'Contact', get_folder(self, 'ContactFolder', 'Contacts'), 'title', contact_name)
        faculty = get_type_or_create(self, 'FacultyMember', get_folder(self, 'FacultyMemberFolder', 'FacultyMembers'), 'title', user_id)
        school = get_type_or_create(self, 'School', get_folder(self, 'SchoolFolder', 'Schools'), 'title', school_name)
        visit = create_object_in_directory(self, get_folder(self,'VisitFolder', 'Visits'), 'Visit')
        
        set_reference(student, visit)
        set_reference(contact, visit)
        set_reference(faculty, visit)
        set_reference(school, visit)
        
        school.edit(title = school_name)
        student.edit(title=student_name, instrument=instrument, email=student_email, phone=student_phone, address=student_address, city=student_city, zip=student_zip)
        contact.edit(title=contact_name, type=contact_title, phone=contact_phone, email=contact_email, isAlumni=is_contact_alumni)
        faculty.edit(title=user_id)
        
        visit_title = "%s-%s-%s-%s" % (school_name, student_name, contact_name, user_id)
        
        visit.edit(title=visit_title, dateOfVisit = date, schools = school, contacts = contact, students = student, facultymembers = faculty)
        