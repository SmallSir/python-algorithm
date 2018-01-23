
#为评论者打分
def topMatcher(person,n=5):
    scores = [(sim_person(person,other),other)for other in critics if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]
