export class User {
  name: string;
  id: string;
  hrm: number;
  admin: number;
  date: string;
  checkin: string;
  checkout: string;
  checkin_number: number;
  checkout_number: number;
  total: number;
}

export class Report {
  id: string;
  workday: Workday[];
  total: number;
  total_days_worked: number;
}

export class IpReport {
  name: string;
  email: string;
  ipcheckin: string[];
  ipcheckout: string[];
}

export class Workday {
  date: string;
  day_of_week: number;
  total: any;
}
