__author__ = 'd.chetverikov'
# The search function returns a list of all words that are less than the given
# maximum distance from the target word
class LeviOnTries:
    @staticmethod
    def search( trie, word, maxCost ):

        # build first row
        currentRow = range( len(word) + 1 )

        results = []

        # recursively search each branch of the trie
        for letter in trie.children:
            LeviOnTries.searchRecursive( trie.children[letter], letter, word, currentRow,
                results, maxCost )

        return results

    # This recursive helper is used by the search function above. It assumes that
    # the previousRow has been filled in already.
    @staticmethod
    def searchRecursive( node, letter, word, previousRow, results, maxCost ):

        columns = len( word ) + 1
        currentRow = [ previousRow[0] + 1 ]

        # Build one row for the letter, with a column for each letter in the target
        # word, plus one for the empty string at column 0
        for column in xrange( 1, columns ):

            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1

            if word[column - 1] != letter:
                replaceCost = previousRow[ column - 1 ] + 1
            else:
                replaceCost = previousRow[ column - 1 ]

            currentRow.append( min( insertCost, deleteCost, replaceCost ) )

        # if the last entry in the row indicates the optimal cost is less than the
        # maximum cost, and there is a word in this trie node, then add it.
        if currentRow[-1] <= maxCost and node.word != None:
            results.append( (node.word, currentRow[-1] ) )

        # if any entries in the row are less than the maximum cost, then
        # recursively search each branch of the trie
        if min( currentRow ) <= maxCost:
            for letter in node.children:
                LeviOnTries.searchRecursive( node.children[letter], letter, word, currentRow,
                    results, maxCost )