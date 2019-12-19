export const rangeFilters = () => ({
  Finance: {
    cost: {
      min: '',
      max: '',
      icon: 'mdi-cash',
      name: 'average_price',
      title: 'Cost $',
      color: '#FFAB91',
    },
    payments: {
      min: '',
      max: '',
      icon: 'mdi-credit-card-outline',
      name: 'monthly_payments',
      title: 'Monthly payments $',
      color: '#DCE775',
    },
    debt: {
      min: '',
      max: '',
      icon: 'mdi-sack-percent',
      name: 'debt_completed_median',
      title: 'Debt after completion $',
      color: '#AED581',
    },
    earnings: {
      min: '',
      max: '',
      icon: 'mdi-currency-usd',
      name: 'median_earnings',
      title: 'Earnings after attending $',
      color: '#80CBC4',
    },
  },
  Aid: {
    pell: {
      min: '',
      max: '',
      icon: 'mdi-cash-100',
      name: 'pell_grand',
      title: 'Pell grant recipients %',
      color: '#FFAB91',
    },
    loan: {
      min: '',
      max: '',
      icon: 'mdi-bank',
      name: 'federal_loan',
      title: 'Federal loan recipients %',
      color: '#DCE775',
    },
  },
  Study: {
    admission: {
      min: '',
      max: '',
      icon: 'mdi-certificate',
      name: 'admission_rate',
      title: 'Admission rate %',
      color: '#AED581',
    },
    completion: {
      min: '',
      max: '',
      icon: 'mdi-school',
      name: 'completion_rate_four_year_pooled',
      title: 'Completion rate %',
      color: '#80CBC4',
    },
    retention: {
      min: '',
      max: '',
      icon: 'mdi-account-heart',
      name: 'retention_rate_four_year_pooled',
      title: 'Retention rate %',
      color: '#FFAB91',
    },
  },
  Tests: {
    act: {
      min: '',
      max: '',
      icon: 'mdi-grease-pencil',
      name: 'act_cumulative',
      title: 'ACT cumulative',
      color: '#DCE775',
    },
    sat: {
      min: '',
      max: '',
      icon: 'mdi-lead-pencil',
      name: 'sat_average',
      title: 'SAT average',
      color: '#AED581',
    },
  },
  Students: {
    undergraduates: {
      min: '',
      max: '',
      icon: 'mdi-account-multiple',
      name: 'undergrad_students',
      title: 'Number of undergraduates',
      color: '#80CBC4',
    },
    fullTime: {
      min: '',
      max: '',
      icon: 'mdi-account-clock',
      name: 'students_part_time',
      title: 'Full-time students %',
      color: '#FFAB91',
    },
    female: {
      min: '',
      max: '',
      icon: 'mdi-human-female',
      name: 'students_female',
      title: 'Female students %',
      color: '#DCE775',
    },
    male: {
      min: '',
      max: '',
      icon: 'mdi-human-male',
      name: 'students_female',
      title: 'Male students %',
      color: '#AED581',
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