export const getCollegesStates = (colleges = []) => {
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

export const filterColleges = (colleges = [], filters = {}) => {
  if (filters.checkboxFilters || filters.statesFilters || filters.rangeFilters) {
    const filteredColleges = colleges.filter((college) => {
      let isFiltered = true;
      if (filters.checkboxFilters) {
        Object.values(filters.checkboxFilters).forEach((filter) => {
          if (filter.value && college[filter.name] === 0) isFiltered = false;
        });
      }
      if (filters.statesFilters && filters.statesFilters.length > 0
         && !filters.statesFilters.some(state => state === college.state__name)) {
        isFiltered = false;
      }
      if (filters.rangeFilters) {
        if (!Object.prototype.hasOwnProperty.call(college, 'average_price')) {
          createUnifiedPriceParam(colleges);
        }
        Object.values(filters.rangeFilters).forEach((filter) => {
          if ((+filter.min && !college[filter.name])
              || (+filter.min && college[filter.name] < +filter.min)) {
            isFiltered = false;
          }
          if ((+filter.max && !college[filter.name])
              || (+filter.max && college[filter.name] > +filter.max)) {
            isFiltered = false;
          }
        });
      }
      return isFiltered;
    });
    return filteredColleges;
  }
  return colleges;
};

export const createUnifiedPriceParam = (colleges = []) => {
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

export const sortNumeric = (colleges = [], param = '', reverseSort = false) => {
  colleges.sort((a, b) => {
    const [first, second] = [a[param], b[param]];
    if (first === null || first === '') return 1;
    if (second === null || second === '') return -1;
    if (!reverseSort) return Number(first) - Number(second);
    return Number(second) - Number(first);
  });
};

export const sortAlphabetically = (colleges = [], reverseSort = false) => {
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
