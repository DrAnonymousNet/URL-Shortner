
interface ITableRow {
  long_url: string;
  short_url: string;
  last_visited: string;
  id: number;
  mutate: KeyedMutator<IUserLinks>;
  // setLink:  React.Dispatch<React.SetStateAction<IUserLink>>
}

interface IReferrer{
  
    [key: string]: number
  
}

interface IDevice {
    // "PC": 2
    [key: string]: number
}
interface IUser {
  email: string,
  password: string,
  confirm_password: string
}

interface SignUpResponse {
  email: string
  id: number
}

interface IUserLinks {
  count: number,
  next: null | number,
  prev: null | number,
  results: IUserLink[]
}

interface IUserLink {
  // url: string,
  id: number,
  short_link: string,
  long_link: string,
  date_created: string,
  last_visited_date: string,
  visit_count: number,
  analytic: {
    date_time_anaylytic:IDateTimeAnalytics

    // today_total: [],
    // "today_by_hour": [],
    // "this_week_by_day": [],
    other_analytic: IOtherAnalytics
  },


}

type CurrentMonth = {
  date: string,
  count__sum: number
}

interface IChartConfig {
  canvasElement: HTMLCanvasElement,
  chartType: ChartType,
  labels: string[],
  data: number[],
  backgroundColor: string[];
  axes: boolean,
  legend: boolean

}
interface IOtherAnalytics{
  Browser: {
    [key: string]: number
    // "Firefox": 2
  },
  OS: {
    // "Windows 10": 2
    [key: string]: number
  },
  Device: IDevice,
  Referer: IReferrer,
  Country: {
    [key: string]: number

  }
}

interface IDateTimeAnalytics{
  current_month: {
    date: string,
    count__sum: number
  }[]
  today_count: {
    date: string,
    count__sum: number
  }[]
  this_week_by_day: {
    date: string,
    count__sum: number
  }[]

  today_by_hour:
  {
    "time__hour": number,
    "count__sum": number
  }[]
}



