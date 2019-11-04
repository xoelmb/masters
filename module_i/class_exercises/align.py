def edit_distance(pattern, text):
    if len(pattern) == 0:
        # Insert all remaining chars
        return len(text)
    elif len(text) == 0:
        # Delete all remaining chars
        return len(pattern)
    else:
        # Find score for match/subtitution
        if pattern[0] == text[0]:
            path.append("M")
            m_cost = edit_distance(pattern[1:], text[1:])
            else:
            m_cost = edit_distance(pattern[1:], text[1:]) + 1
        # Find score for insertion
        i_cost = edit_distance(pattern[:], text[1:]) + 1
        # Find score for deletion
        d_cost = edit_distance(pattern[1:], text[:]) + 1
        # Find the minimum combination
        return min(m_cost, i_cost, d_cost)


path=[]
pattern = "ATC"
text = "TC"
distance = edit_distance(pattern, text)
print(distance)  # Prints "1"
