import {ISchedule} from "../interfaces/types.ts";


const weekDays = [
    'Lunes',
    'Martes',
    'Miércoles',
    'Jueves',
    'Viernes',
    'Sábado',
    'Domingo',
]

function formatHoursToHAMPM(hours: number): string {
    const date = new Date();
    date.setHours(hours);
    const options: Intl.DateTimeFormatOptions = {
        hour: 'numeric',
        hour12: true,
    };
    return date.toLocaleTimeString('en-EN', options);
}
interface Props {
    blockSchedules: ISchedule[]
}
export function Schedule({blockSchedules}: Props) {
    return (
        <div className={'flex flex-col space-y-4'}>
            <h1 className={'text-2xl font-bold text-slate-800'}>Programación de cortes</h1>
            <div className={'grid grid-cols-3 gap-x-4 gap-y-10'}>
                {blockSchedules.map((schedule, index) => (
                    <div key={index}
                         className={'flex flex-col space-y-2 p-5 border-2 bg-indigo-50 border-indigo-600 rounded-md'}>
                        <h3 className={'text-lg font-bold text-indigo-700'}>Bloque {schedule.blockNumber}</h3>
                        <div className={'flex flex-col space-y-2'}>
                            {schedule.schedule.map((s, idx) => (
                                <h4 key={idx} className={'text-base font-semibold text-slate-800'}>
                                    <span className={'font-bold'}>{weekDays[s.dayOfWeek]}</span>: <span className={'italic text-sm'}>{formatHoursToHAMPM(s.startCut)} - {formatHoursToHAMPM(s.endCut)}</span>
                                </h4>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}