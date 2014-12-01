
def mail_by_instrument_type(self, instrument, student_name, school_name, link):
    
    pm = self.portal_membership
    
    if len(instrument) > 0:

        for member_id in pm.listMemberIds():
        
            member = pm.getMemberById(member_id)

            user_instruments = map(lambda x: x.lower().strip(), member.getProperty('instrument', None).split(','))        
        
            if instrument in user_instruments and \
               member != self.portal_membership.getAuthenticatedMember().id and \
               member.getProperty('email', None):
        
                mail_host = self.MailHost
                to_addr   = member.getProperty('email', None)
                from_addr = "music.recruiting@uwosh.edu"
                subj = 'A student of interest has been added to the Music Recruiting Website!'
        
                body = """
        
                Student:     %s
                School:      %s
                Instrument:  %s
                Link:        %s
                
                """ % (student_name, school_name, instrument , link)
                
        
                self.MailHost.secureSend(body, to_addr, from_addr, subj)