export class User {
  name: string;
  id: string;
  date: string;
  checkin: string;
  checkout: string;
  total: number;
}

export class Report {
  id: string;
  workday: Workday[];
  total: number;
  total_days_worked: number;
}

export class Workday {
  date: string;
  day_week: number;
  total: any;
}