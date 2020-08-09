        date_level = False
        for t in timeline_tags:
#                print('1', self.timebuckets)
            self.timebuckets = {} if (self.timebuckets is None) else self.timebuckets
#                print('2', self.timebuckets)
            if t.a:
                l = t.a.string 
                u = t.a['href']
                if bucket_url == u: # When we reach a date and click or navigate to it, the markup stays the same. Exit here
                    for t in timeline_tags:
                        if t.a:
                            l = t.a.string 
                            u = t.a['href']
                            print('DATE    ', l, u)
                    date_level = True
                    break
                if date_level != True:
                    self.timebuckets[l] = u
                    print('L,U     ', l, u, date_level)
                    return self.get_timebuckets(l, u)
            else:
                continue
        
#        print(self.timebuckets)