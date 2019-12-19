// Creates a list of states' names from selected colleges
export const getCollegesStatesNames = (colleges = []) => {
  const states = [];
  colleges.forEach((college) => {
    if (!states.some(state => state === college.state__name)) states.push(college.state__name);
    states.sort((a, b) => {
      if (a.toLowerCase() < b.toLowerCase()) return -1;
      if (a.toLowerCase() > b.toLowerCase()) return 1;
      return 0;
    });
  });
  return states;
};

// Applies filters to the list of colleges
export const selectColleges = (colleges = [], filters = {}) => {
  if (Object.keys(filters).length > 0) {
    const selectedColleges = colleges.filter((college) => {
      let isSelected = true;
      // apply checkbox filter
      if (filters.checkboxFilters) {
        Object.values(filters.checkboxFilters).forEach((filter) => {
          if (filter.value && college[filter.name] === 0) isSelected = false;
        });
      }
      // apply state filter
      if (filters.statesFilters && filters.statesFilters.length > 0
         && !filters.statesFilters.some(state => state === college.state__name)) {
        isSelected = false;
      }
      // apply range filter
      if (filters.rangeFilters) {
        // to filter colleges by price parameter we need to add a new parameter which will
        // contain either average_net_price_private or average_net_price_public value
        if (!Object.prototype.hasOwnProperty.call(college, 'average_price')) {
          addUnifiedPriceParam(colleges);
        }
        Object.values(filters.rangeFilters).forEach((filter) => {
          if ((+filter.min && !college[filter.name])
              || (+filter.min && college[filter.name] < +filter.min)) {
            isSelected = false;
          }
          if ((+filter.max && !college[filter.name])
              || (+filter.max && college[filter.name] > +filter.max)) {
            isSelected = false;
          }
        });
      }
      return isSelected;
    });
    return selectedColleges;
  }
  return colleges;
};

/*
* As private colleges store average price value in an average_net_price_private parameter
* and public colleges store it in an average_net_price_public parameter, we need to add a new
* parameter which will contain either average_net_price_private or average_net_price_public value.
* This new parameter's name is average_price which will be used to filter colleges by price.
* */
export const addUnifiedPriceParam = (colleges = []) => {
  colleges.forEach((college) => {
    if (!college.average_net_price_public) {
      // eslint-disable-next-line no-param-reassign
      college.average_price = college.average_net_price_private;
    }
    if (!college.average_net_price_private) {
      // eslint-disable-next-line no-param-reassign
      college.average_price = college.average_net_price_public;
    }
  });
};

// https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
export const addCommas = (num) => {
  try {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  } catch (e) {
    return '';
  }
};

// Sorts colleges by any numeric parameter. Ascending by default
export const sortByNumValue = (colleges = [], param = '', reverseSort = false) => {
  colleges.sort((a, b) => {
    const [first, second] = [a[param], b[param]];
    if (first === null || first === '') return 1;
    if (second === null || second === '') return -1;
    if (!reverseSort) return Number(first) - Number(second);
    return Number(second) - Number(first);
  });
};

// Sorts colleges by name. Ascending by default
export const sortСollegesAlphabetically = (colleges = [], reverseSort = false) => {
  colleges.sort((a, b) => {
    if (a.name.toLowerCase() < b.name.toLowerCase()) {
      if (!reverseSort) return -1;
      return 1;
    }
    if (a.name.toLowerCase() > b.name.toLowerCase()) {
      if (!reverseSort) return 1;
      return -1;
    }
    return 0;
  });
};

export const sortColleges = (component) => {
  if (!component.selectedColleges) component.updateFilteredCollegesList();
  // set isReverseSort variable to true on the same button click
  if (component.menu.prevSortButton.name === component.menu.activeSortButton.name) {
    // eslint-disable-next-line no-param-reassign
    component.isReverseSort = !component.isReverseSort;
  } else {
    // eslint-disable-next-line no-param-reassign
    component.isReverseSort = false;
  }
  switch (component.menu.activeSortButton.name) {
  case 'name':
    sortСollegesAlphabetically(component.selectedColleges, component.isReverseSort);
    break;
  case 'average_price':
    component.sortByCost();
    break;
  case 'federal_loan':
  case 'admission_rate':
  case 'undergrad_students':
    sortByNumValue(component.selectedColleges, component.menu.activeSortButton.name,
      component.isReverseSort);
    break;
  default:
    break;
  }
};