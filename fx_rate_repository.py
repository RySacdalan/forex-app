from file_repository import FileRepository
import json
from fx_rate_utils import FxRateUtils

class FxRateRepository(FileRepository):
    utils = FxRateUtils
    fx_rate = None
    
    def __init__(self) -> None:
        super().__init__("fx-rate.json")
        
    # get all fx rate in json
    def get_fx_rate(self):
        if self.fx_rate == None:
            self.fx_rate = json.loads(super().readFile())
        return self.fx_rate
    
    # add new fx rate in json
    def add_new_fx_rate(self, fx_entry):
        fx_entry["id"] = self.utils.generateId(self)
        self.get_fx_rate()["currencies"].append(fx_entry)
        self.save()
        
    # update existing rate in json
    def update_fx_rate(self, fx_entry):
        result = list(filter(lambda entry: entry.get("id") == fx_entry.get("id"), self.get_fx_rate()["currencies"]))
        result[0] = fx_entry
        self.save()
        print("Updated Successfully!")
    
    # delete existing rate in json
    def delete_fx_rate(self, fx_rate):
        index = 0
        for entry in self.get_fx_rate()["currencies"]:
            if entry.get("id") == fx_rate.get("id"):
                break
            index = index + 1
        self.get_fx_rate()["currencies"].pop(index)
        self.save()
        
    # save new fx rate to json
    def save(self):
        super().writeFile(json.dumps(self.fx_rate))
        
    # finding existing rate 
    def find_fx_rate(self, base_curr, foreign_curr):
        result = []
        base_curr = base_curr.lower()
        foreign_curr = foreign_curr.lower()
        stringComparer = lambda a,b : (a.lower() == b or b == "")
        
        for entry in self.get_fx_rate()["currencies"]:
            # if (entry.get("baseCurr", "").lower() == base_curr or base_curr == "") and (entry.get("foreign", "").lower() == foreign_curr or foreign_curr == ""):
            if stringComparer(entry.get("baseCurr", ""), base_curr) and stringComparer(entry.get("foreign", ""), foreign_curr):
                result.append(entry)
                result = list(filter(lambda entry: stringComparer(entry.get("baseCurr", ""), base_curr) and stringComparer(entry.get("foreign", ""), foreign_curr), self.get_fx_rate()["currencies"]))
        return result