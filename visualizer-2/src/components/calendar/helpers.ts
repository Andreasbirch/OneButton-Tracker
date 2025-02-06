import { Press } from "../../models/patients/PatientData";

//https://stackoverflow.com/questions/42136098/array-groupby-in-typescript
export  const groupBy = <T, K extends keyof any>(list: T[], getKey: (item: T) => K) =>
    list.reduce((previous, currentItem) => {
      const group = getKey(currentItem);
      if (!previous[group]) previous[group] = [];
      previous[group].push(currentItem);
      return previous;
    }, {} as Record<K, T[]>);

//https://weeknumber.com/how-to/javascript
export function getWeek(dt: Date) {
    let date = new Date(dt);
    date.setHours(0, 0, 0, 0);
    // Thursday in current week decides the year.
    date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
    // January 4 is always in week 1.
    var week1 = new Date(date.getFullYear(), 0, 4);
    // Adjust to Thursday in week 1 and count number of weeks from date to week1.
    return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
                          - 3 + (week1.getDay() + 6) % 7) / 7);
};

export function timeFloat(timestamp: Date) {
    const hours = new Date(timestamp).getHours();
    const minutes = new Date(timestamp).getMinutes();
    return hours + minutes / 60;
  };

// https://stackoverflow.com/questions/4413590/javascript-get-array-of-dates-between-2-dates
export function getDaysArray(s: Date,e: Date) {const a=[];for(const d=new Date(s);d<=new Date(e);d.setDate(d.getDate()+1)){ a.push(new Date(d));}return a;};


// Function to get color based on the count
const oranges = ["#fff5eb","#fff5ea","#fff4e9","#fff4e8","#fff3e7","#fff3e6","#fff2e6","#fff2e5","#fff1e4","#fff1e3","#fff0e2","#fff0e1","#ffefe0","#ffefdf","#ffeede","#ffeedd","#feeddc","#feeddb","#feecda","#feecd9","#feebd8","#feebd7","#feead6","#feead5","#fee9d4","#fee9d3","#fee8d2","#fee8d1","#fee7d0","#fee6cf","#fee6ce","#fee5cc","#fee5cb","#fee4ca","#fee4c9","#fee3c8","#fee2c7","#fee2c5","#fee1c4","#fee1c3","#fee0c2","#fedfc0","#fedfbf","#fedebe","#feddbd","#feddbb","#fedcba","#fedbb9","#fedab7","#fddab6","#fdd9b4","#fdd8b3","#fdd8b2","#fdd7b0","#fdd6af","#fdd5ad","#fdd4ac","#fdd4aa","#fdd3a9","#fdd2a7","#fdd1a6","#fdd0a4","#fdd0a3","#fdcfa1","#fdcea0","#fdcd9e","#fdcc9d","#fdcb9b","#fdca99","#fdc998","#fdc896","#fdc795","#fdc693","#fdc591","#fdc490","#fdc38e","#fdc28d","#fdc18b","#fdc089","#fdbf88","#fdbe86","#fdbd84","#fdbc83","#fdbb81","#fdba7f","#fdb97e","#fdb87c","#fdb77a","#fdb679","#fdb577","#fdb475","#fdb374","#fdb272","#fdb171","#fdb06f","#fdaf6d","#fdae6c","#fdad6a","#fdac69","#fdab67","#fdaa65","#fda964","#fda762","#fda661","#fda55f","#fda45e","#fda35c","#fda25b","#fda159","#fda058","#fd9f56","#fd9e55","#fd9d53","#fd9c52","#fd9b50","#fd9a4f","#fc994d","#fc984c","#fc974a","#fc9649","#fc9548","#fc9346","#fc9245","#fc9143","#fc9042","#fb8f40","#fb8e3f","#fb8d3e","#fb8c3c","#fb8b3b","#fa8a3a","#fa8938","#fa8837","#fa8736","#fa8534","#f98433","#f98332","#f98230","#f8812f","#f8802e","#f87f2c","#f77e2b","#f77d2a","#f77b29","#f67a27","#f67926","#f57825","#f57724","#f57623","#f47522","#f47420","#f3731f","#f3721e","#f2701d","#f26f1c","#f16e1b","#f16d1a","#f06c19","#f06b18","#ef6a17","#ef6916","#ee6815","#ed6714","#ed6614","#ec6513","#ec6312","#eb6211","#ea6110","#ea6010","#e95f0f","#e85e0e","#e85d0e","#e75c0d","#e65b0c","#e55a0c","#e4590b","#e4580b","#e3570a","#e25609","#e15509","#e05408","#df5308","#de5208","#dd5207","#dc5107","#db5006","#da4f06","#d94e06","#d84d05","#d74c05","#d64c05","#d54b04","#d44a04","#d24904","#d14804","#d04804","#cf4703","#cd4603","#cc4503","#cb4503","#c94403","#c84303","#c74303","#c54203","#c44103","#c24102","#c14002","#bf3f02","#be3f02","#bd3e02","#bb3e02","#ba3d02","#b83d02","#b73c02","#b53b02","#b43b02","#b23a03","#b13a03","#af3903","#ae3903","#ac3803","#ab3803","#aa3703","#a83703","#a73603","#a53603","#a43503","#a33503","#a13403","#a03403","#9f3303","#9d3303","#9c3203","#9b3203","#993103","#983103","#973003","#953003","#942f03","#932f03","#922e04","#902e04","#8f2d04","#8e2d04","#8d2c04","#8b2c04","#8a2b04","#892b04","#882a04","#862a04","#852904","#842904","#832804","#812804","#802704","#7f2704"];
export function getColor(groups: Record<string, Press[]>, date: Date): string | null {
  if(!date) 
      return null;
  
  const dateString = date.toISOString().split('T')[0];
  const group = groups[dateString];

  if (!group)
    return null;

  const count = group.length;
  const maxCount = Math.max(...Object.values(groups).map(o => o.length))
  const normalizedIndex = Math.min(Math.max(0, Math.floor((count / maxCount) * 255)), 255); // Normalize to 0-255 range
  
  // Return the color from the oranges array
  return oranges[normalizedIndex];
}

// Trims gaps which the target date starts in, ends in, or if the gap is wholly within said date
// https://www.typescriptlang.org/docs/handbook/2/generics.html
export function GetGapIntersectForDate<T extends { start: Date; end: Date }>(
  gaps: T[],
  date: Date
): T[] {
  const targetDate = new Date(date);
  const nextDate = new Date(targetDate);
  nextDate.setDate(nextDate.getDate() + 1);

  const startOfDay = new Date(targetDate);
  startOfDay.setHours(0, 0, 0, 0);

  const endOfDay = new Date(nextDate);
  endOfDay.setMilliseconds(-1); // Just before midnight of the next day

  return gaps
      .filter(gap => {
          const gapStart = new Date(gap.start);
          const gapEnd = new Date(gap.end);
          return gapStart < endOfDay && gapEnd > startOfDay;
      })
      .map(gap => {
          const gapStart = new Date(gap.start);
          const gapEnd = new Date(gap.end);

          const adjustedStart = gapStart < startOfDay ? startOfDay : gapStart;
          const adjustedEnd = gapEnd > endOfDay ? endOfDay : gapEnd;

          return {
              ...gap,
              start: adjustedStart,
              end: adjustedEnd
          };
      });
}
