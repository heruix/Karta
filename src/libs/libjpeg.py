from lib_template import *
import string

class LibJPEGSeeker(Seeker):
    # Library Name
    NAME = 'libjpeg'
    # version string marker
    VERSION_STRING = ", Thomas G. Lane, Guido Vollbeding"

    # Overriden base function
    def searchLib(self, logger):
        # Now search
        self._version_strings = []
        for bin_idx, bin_str in enumerate(self._all_strings):
            # we have a match
            if self.VERSION_STRING in str(bin_str) and bin_idx + 1 < len(self._all_strings) :
                # double check it
                wanted_string_raw = self._all_strings[bin_idx + 1]
                wanted_string = str(wanted_string_raw)
                try :
                    if wanted_string.count("-") == 2 and len(wanted_string.split("-")[-1]) == 4:
                        year = int(wanted_string.split("-")[-1])
                    # if both libraries (Karta and libjpeg) will be used in 2100, we will other things to worry about
                    if year < 1900 or 2100 < year :
                        continue
                except :
                    continue
                # valid match
                logger.debug("Located a version string of %s in address 0x%x", self.NAME, wanted_string_raw.ea)
                # save the string for later
                self._version_strings.append(wanted_string)

        # return the result
        return len(self._version_strings)

    # Overriden base function
    def identifyVersions(self, logger):
        results = []
        # extract the version from the copyright string
        for work_str in self._version_strings:
            results.append(self.extractVersion(work_str, legal_chars = string.digits + string.ascii_lowercase + '.'))
        # return the result
        return results

# Register our class
LibJPEGSeeker.register(LibJPEGSeeker.NAME, LibJPEGSeeker)