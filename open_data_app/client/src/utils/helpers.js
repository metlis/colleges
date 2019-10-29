const getCollegesStates = (colleges) => {
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

export default getCollegesStates;