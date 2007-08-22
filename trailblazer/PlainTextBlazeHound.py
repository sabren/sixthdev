from Solution import Solution


def parseBlaze(line, prefix):
    return line[line.find(prefix)+len(prefix):].strip()


def loadTBFile(fileName, blaze="@:"):

    openTag = blaze
    closeTag = blaze+"/"

    top = currentSolution = Solution()
    top.fileName = fileName
    
    
    currentName = ""
    stack = []

    for lineNumber, line in enumerate(open(fileName)):

        # check for / first because the match is more specific
        if line.count(closeTag):
            name = parseBlaze(line, closeTag)
            assert name == currentName, (
                   "mismatched end tag (%s vs %s) on line %s of %s"
                   % (name, currentName, lineNumber+1, top.fileName))
            
            currentName, currentSolution = stack.pop()

        elif line.count(openTag):
            stack.append((currentName, currentSolution))
            currentName = parseBlaze(line, openTag)
            currentSolution = currentSolution.blaze(currentName)
            

        else:
            currentSolution.append(line)

    assert stack == [], "expected close tag for %s" % currentName

    return top
