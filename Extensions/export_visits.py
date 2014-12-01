import csv, StringIO, time

def export_all_visits(self):
  text = StringIO.StringIO()

  writer = csv.writer(text, delimiter=",")

  visits = self.queryCatalog({'portal_type':'Visit'})

  header = ['School', 'Student Name', 'Instrument', 'Student Email', 'Student Phone', 'Student Address', 'Student City',
            'Student Zip', 'Contact Name', 'Contact Title', 'Contact Phone', 'Contact Email', 'Is Contact Alumni', 'Date']
  writer.writerow(header)
  
  for visit in visits:
    visit_props = []
    
    visit = visit.getObject()
    
    school = visit.getSchools()
    visit_props.append(school.Title())
    
    student = visit.getStudents()
    visit_props.append(student.Title())
    visit_props.append(student.getInstrument())
    visit_props.append(student.getEmail())
    visit_props.append(student.getPhone())
    visit_props.append(student.getAddress())
    visit_props.append(student.getCity())
    visit_props.append(student.getZip())
    
    contact = visit.getContacts()
    visit_props.append(contact.Title())
    visit_props.append(contact.getType())
    visit_props.append(contact.getPhone())
    visit_props.append(contact.getEmail())
    visit_props.append(contact.getIsAlumni())
    
    visit_props.append(visit.getDateOfVisit())

    writer.writerow(visit_props)


  self.REQUEST.RESPONSE.setHeader('Content-Type','application/csv')
  self.REQUEST.RESPONSE.setHeader('Content-Length',len(text.getvalue()))
  self.REQUEST.RESPONSE.setHeader('Content-Disposition','inline;filename=%sstudents.csv' %
                                time.strftime("%Y%m%d-%H%M%S-",time.localtime()))

  return text.getvalue()

def export_user_visits(self):
  
  pm = self.portal_membership
  user = pm.getAuthenticatedMember()
  
  text = StringIO.StringIO()

  writer = csv.writer(text, delimiter=",")

  visits = self.queryCatalog({'portal_type':'Visit', 'creator':user.id})

  header = ['School', 'Student Name', 'Instrument', 'Student Email', 'Student Phone', 'Student Address', 'Student City',
            'Student Zip', 'Contact Name', 'Contact Title', 'Contact Phone', 'Contact Email', 'Is Contact Alumni', 'Date']
  writer.writerow(header)
  
  for visit in visits:
    visit_props = []
    
    visit = visit.getObject()
    
    school = visit.getSchools()
    visit_props.append(school.Title())
    
    student = visit.getStudents()
    visit_props.append(student.Title())
    visit_props.append(student.getInstrument())
    visit_props.append(student.getEmail())
    visit_props.append(student.getPhone())
    visit_props.append(student.getAddress())
    visit_props.append(student.getCity())
    visit_props.append(student.getZip())
    
    contact = visit.getContacts()
    visit_props.append(contact.Title())
    visit_props.append(contact.getType())
    visit_props.append(contact.getPhone())
    visit_props.append(contact.getEmail())
    visit_props.append(contact.getIsAlumni())
    
    visit_props.append(visit.getDateOfVisit())

    writer.writerow(visit_props)


  self.REQUEST.RESPONSE.setHeader('Content-Type','application/csv')
  self.REQUEST.RESPONSE.setHeader('Content-Length',len(text.getvalue()))
  self.REQUEST.RESPONSE.setHeader('Content-Disposition','inline;filename=%sstudents.csv' %
                                time.strftime("%Y%m%d-%H%M%S-",time.localtime()))

  return text.getvalue()