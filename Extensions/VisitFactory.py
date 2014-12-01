from Products.PythonScripts.standard import url_quote, urlencode
import transaction

class VisitFactory:
    '''A Class that will handle the creation of visit objects and corresponding schools, students, contacts, etc'''

    context = None
    request = None
    visit = None
    save_point = transaction.savepoint()
    state = None
    new_visit = True
    
    def __init__(self, context, state):
        self.context = context
        self.request = context.REQUEST
        self.state = state
        
    def create_visit_and_references(self):
        self.create_visit()
        self.create_school()
        self.create_contact()
        self.create_faculty()
        
        self.set_next_action()
        
        self.mail_appropriate_faculty()
    
    def create_visit(self):
        '''Creates visit to work with'''
        
        visit_id = self.request.get('id')

        #check if id has already been generated
        if visit_id:
            #check if it is just editing existing visit
            old_visits = self.context.queryCatalog({'portal_type':'Visit', 'id':visit_id})
            if len(old_visits) is 0:
                self.visit = create_with_id_object_in_directory(get_folder('VisitFolder', 'Visits'), 'Visit', visit_id)
            else:
                self.visit = old_visits[0].getObject()
                self.new_visit = False
        else:
            self.visit = create_object_in_directory(get_folder('VisitFolder', 'Visits'), 'Visit')
            
        self.set_date_and_notes()

    def create_school(self):
        school_folder = self.get_folder('SchoolFolder', 'Schools')

        if self.request.get('school_title'):
            
            new_school = self.create_object_in_directory(school_folder, 'School')

            new_school.edit(title=self.request.get('school_title'))
            self.visit.edit(title=new_school.Title(), schools = new_school)

            self.set_reference(new_school)

        elif len(self.request.get('schools_drop_down')) > 0:
            
            existing_school = school_folder[self.request.get('schools_drop_down')]
            self.set_reference(existing_school)
            self.visit.edit(title=existing_school.Title(), schools=existing_school)

    def create_student(self):
        if self.request.get('student_title'):

            student_folder = self.get_folder('StudentFolder', 'Students')
            new_student = self.create_object_in_directory(student_folder, 'Student')

            is_committed = False
            if self.request.get('isCommittedToAttend'):
                is_committed = True

            items = ['student_title', 'student_phone', 'student_email', 'student_instrument', 'student_address', 'student_city', 'student_zip']
            request_items = self.get_request_items(items)

            new_student.edit(title      = request_items['student_title'], \
                             phone      = request_items['student_phone'], \
                             email      = request_items['student_email'], \
                             instrument = request_items['student_instrument'], \
                             address    = request_items['student_address'], \
                             city       = request_items['student_city'], \
                             zip        = request_items['student_zip'], \
                             isCommittedToAttend = is_committed)

            self.set_reference(new_student)

            self.visit.edit(title = new_visit.Title() + '-' + new_student.Title(), students = new_student)

        elif len(self.request.get('students_drop_down')) > 0:
            existing_student = get_folder('StudentFolder', 'Students')[self.request.get('students_drop_down')]

            set_reference(existing_student)

            name = self.visit.Title() + '-' + existing_student.Title()
            self.visit.edit(title = name, students = existing_student)
        
    def create_contact(self):
        #Create Contact and add to Visit  
        contact_folder = self.get_folder('ContactFolder', 'Contacts')
        if self.request.get('contact_title'):

            new_contact = self.create_object_in_directory(contact_folder, 'Contact')

            is_alumni = False
            if self.request.get('contact_isAlumni'):
                is_alumni = True

            items = ['contact_title', 'contact_type', 'contact_phone', 'contact_email', 'contact_address', 'contact_city', 'contact_state', 'contact_zip']
            request_items = self.get_request_items(items)

            new_contact.edit(title      = request_items['contact_title'], \
                             type       = request_items['contact_type'], \
                             phone      = request_items['contact_phone'], \
                             email      = request_items['contact_email'], \
                             address    = request_items['contact_address'], \
                             city       = request_items['contact_city'], \
                             state      = request_items['contact_state'], \
                             zip        = request_items['contact_zip'], \
                             isAlumni   = is_alumni)

            self.set_reference(new_contact)

            name = self.visit.Title() + '-' + new_contact.Title()
            new_visit.edit(title = name, contacts = new_contact)

        elif len(self.request.get('contacts_drop_down')) > 0:

            existing_contact = contact_folder[self.request.get('contacts_drop_down')]

            self.set_reference(existing_contact)

            name = self.visit.Title() + '-' + existing_contact.Title()
            self.visit.edit(title = name, contacts = existing_contact)
    
    def create_faculty(self):
        faculty_dd_id = self.request.get('facultymembers_drop_down')
        faculty_field_id = self.request.get('facultymember_title')
        user_id = self.context.portal_membership.getAuthenticatedMember().id
        faculty_folder = self.get_folder('FacultyMemberFolder', 'FacultyMembers')
    
        #Create Faculty and add to visit
        if faculty_dd_id is faculty_field_id:
            existing_faculty = self.get_folder('FacultyMemberFolder', 'FacultyMembers')[faculty_dd_id]

            self.set_reference(existing_faculty)

            name = self.visit.Title() + '-' + existing_faculty.getName()
            self.visit.edit(title = name, facultymembers = existing_faculty)

        elif  len(faculty_dd_id) > 0:
            existing_faculty = self.context.queryCatalog({'portal_type':'FacultyMember', 'id':faculty_dd_id})
            faculty = None

            if len(existing_faculty) > 0:
                faculty = existing_faculty[0]
                faculty = faculty.getObject()

                if faculty.getEmail() != self.request.get('facultymember_email'):
                    faculty.edit(email = self.request.get('facultymember_email'))

                self.set_reference(faculty)
            else:
                faculty  = self.create_object_in_directory(faculty_folder, 'FacultyMember')
                faculty.edit(title = self.request.get('facultymember_title'), email = self.request.get('facultymember_email'))

                self.set_reference(faculty)

            self.visit.edit(title = self.visit.Title() + '-' + faculty.Title(), facultymembers = faculty)

        else:
            existing_faculty = self.context.queryCatalog({'portal_type':'FacultyMember', 'title':faculty_field_id})
            faculty = None

            if len(existing_faculty) > 0:
                faculty = existing_faculty[0]
                faculty = faculty.getObject()

                if faculty.getEmail() != self.request.get('facultymember_email'):
                    faculty.edit(email = self.request.get('facultymember_email'))

                self.set_reference(faculty)

            else:
                faculty  = create_object_in_directory(faculty_folder, 'FacultyMember')
                faculty.edit(title = self.request.get('facultymember_title'), email = self.request.get('facultymember_email'))

                self.set_reference(faculty)

            self.visit.edit(title = self.visit.Title() + '-' + faculty.Title(), facultymembers = faculty)
        
    def set_date_and_notes(self):
        date =  self.request.get('dateOfVisit_year') + '/' + \
                self.request.get('dateOfVisit_month') + '/' + \
                self.request.get('dateOfVisit_day') + ' ' + \
                self.request.get('dateOfVisit_hour') + ':' + \
                self.request.get('dateOfVisit_minute') + ' ' + \
                self.request.get('dateOfVisit_ampm')
        
        self.visit.edit(notes = self.request.get('notes'), dateOfVisit = date)
    
    def set_next_action(self):

        self.state.setNextAction ('redirect_to:string:' + self.get_link_to_visit())
        
    def mail_appropriate_faculty(self):
        instrument = None
        student_name = None

        if self.request.get('student_title'):
            instrument = self.request.get('student_instrument')
            student_name = self.request.get('student_title')
        else:
            existing_contact = self.get_folder('StudentFolder', 'Students')[self.request.get('students_drop_down')]
            instrument = existing_contact.getInstrument()
            student_name = existing_student.Title()


        #email professors who have the selected instrument in their preferences
        if instrument and student_name and self.new_visit:
            school_name = None
            if self.context.REQUEST.get('school_title'):
                school_name = self.request.get('school_title')
            else:
                school_name = self.get_folder('SchoolFolder', 'Schools')[self.request.get('schools_drop_down')].Title()

            self.context.mail_by_instrument_type(instrument, student_name, school_name, self.get_link_to_visit())
        
    def get_link_to_visit(self):
        return self.context.portal_url.getPortalObject().absolute_url() + '/' + \
             self.get_folder('VisitFolder', 'Visits').id + '/' + self.visit.id
    
    def get_state(self):
        return state
    
    def get_request_items(self, item_list):
        request = {}
        for item in item_list
            request[item] = self.request.get(item)
            
        return request
        
    def get_folder(self, type, name):
        folder_queried = context.queryCatalog({'portal_type':type, 'title':name})[0]
        return folder_queried.getObject()

    def create_object_in_directory(self, container, type):
        id = container.generateUniqueId(type)
        container.invokeFactory(id=id, type_name=type)
        return container[id]

    def create_with_id_object_in_directory(self, container, type, id):
        container.invokeFactory(id=id, type_name=type)
        return container[id]

    def set_reference(self, object):
        existing_visits = object.getVisits()

        if visit not in existing_visits:
            existing_visits.append(self.visit)
            object.setVisits(existing_visits)

visit_factory = VisitFactory(context, state)
visit_factory.create_visit_and_references()

return vist_factory.getState()