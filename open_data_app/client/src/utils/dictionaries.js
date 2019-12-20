export const rangeFilters = () => ({
  Finance: {
    cost: {
      min: '',
      max: '',
      icon: 'mdi-cash',
      name: 'average_price',
      title: 'Cost $',
      color: '#CFD8DC',
    },
    payments: {
      min: '',
      max: '',
      icon: 'mdi-credit-card-outline',
      name: 'monthly_payments',
      title: 'Monthly payments $',
      color: '#CFD8DC',
    },
    debt: {
      min: '',
      max: '',
      icon: 'mdi-sack-percent',
      name: 'debt_completed_median',
      title: 'Debt after completion $',
      color: '#CFD8DC',
    },
    earnings: {
      min: '',
      max: '',
      icon: 'mdi-currency-usd',
      name: 'median_earnings',
      title: 'Earnings after attending $',
      color: '#CFD8DC',
    },
  },
  Aid: {
    pell: {
      min: '',
      max: '',
      icon: 'mdi-cash-100',
      name: 'pell_grand',
      title: 'Pell grant recipients %',
      color: '#CFD8DC',
    },
    loan: {
      min: '',
      max: '',
      icon: 'mdi-bank',
      name: 'federal_loan',
      title: 'Federal loan recipients %',
      color: '#CFD8DC',
    },
  },
  Study: {
    admission: {
      min: '',
      max: '',
      icon: 'mdi-certificate',
      name: 'admission_rate',
      title: 'Admission rate %',
      color: '#CFD8DC',
    },
    completion: {
      min: '',
      max: '',
      icon: 'mdi-school',
      name: 'completion_rate_four_year_pooled',
      title: 'Completion rate %',
      color: '#CFD8DC',
    },
    retention: {
      min: '',
      max: '',
      icon: 'mdi-account-heart',
      name: 'retention_rate_four_year_pooled',
      title: 'Retention rate %',
      color: '#CFD8DC',
    },
  },
  Tests: {
    act: {
      min: '',
      max: '',
      icon: 'mdi-grease-pencil',
      name: 'act_cumulative',
      title: 'ACT cumulative',
      color: '#CFD8DC',
    },
    sat: {
      min: '',
      max: '',
      icon: 'mdi-lead-pencil',
      name: 'sat_average',
      title: 'SAT average',
      color: '#CFD8DC',
    },
  },
  Students: {
    undergraduates: {
      min: '',
      max: '',
      icon: 'mdi-account-multiple',
      name: 'undergrad_students',
      title: 'Number of undergraduates',
      color: '#CFD8DC',
    },
    fullTime: {
      min: '',
      max: '',
      icon: 'mdi-account-clock',
      name: 'students_part_time',
      title: 'Full-time students %',
      color: '#CFD8DC',
    },
    female: {
      min: '',
      max: '',
      icon: 'mdi-human-female',
      name: 'students_female',
      title: 'Female students %',
      color: '#CFD8DC',
    },
    male: {
      min: '',
      max: '',
      icon: 'mdi-human-male',
      name: 'students_female',
      title: 'Male students %',
      color: '#CFD8DC',
    },
  },
});

export const checkboxFilters = () => ({
  operating: {
    value: false,
    name: 'cur_operating',
    title: 'Operating',
  },
  online: {
    value: false,
    name: 'online_only',
    title: 'Online-only',
  },
  men: {
    value: false,
    name: 'men_only',
    title: 'Men-only',
  },
  women: {
    value: false,
    name: 'women_only',
    title: 'Women-only',
  },
  black: {
    value: false,
    name: 'predom_black',
    title: 'Black',
  },
  hispanic: {
    value: false,
    name: 'hispanic',
    title: 'Hispanic',
  },
});

export const sortNames = () => ({
  name: {
    icon: 'mdi-alphabetical',
    title: 'Name',
    tooltip: 'Name',
    name: 'name',
  },
  cost: {
    icon: 'mdi-cash',
    title: 'Cost',
    tooltip: 'Average cost $',
    name: 'average_price',
  },
  loan: {
    icon: 'mdi-bank',
    title: 'Loan',
    tooltip: 'Federal loan recipients %',
    name: 'federal_loan',
  },
  admission: {
    icon: 'mdi-certificate',
    title: 'Admission',
    tooltip: 'Admission rate %',
    name: 'admission_rate',
  },
  undergraduates: {
    icon: 'mdi-account-multiple',
    title: 'Undergraduates',
    tooltip: 'Number of undergraduate students',
    name: 'undergrad_students',
  },
});