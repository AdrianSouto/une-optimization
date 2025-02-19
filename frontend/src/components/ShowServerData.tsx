import {IServerDataResponse} from "../interfaces/types.ts";

export default function ShowServerData({data}: {data: IServerDataResponse}){

    return (
        <div className={'flex flex-col space-y-4'}>
            <h1 className={'text-2xl font-bold text-slate-800'}>Resultados del modelo</h1>
            <div className={'flex flex-col space-y-2'}>
                <h2 className={'text-lg font-semibold text-slate-800'}>Demanda Total: {data.totalDemand} MW</h2>
                <h2 className={'text-lg font-semibold text-slate-800'}>Generación Total: {data.totalGeneration} MW</h2>
                <h2 className={'text-lg font-semibold text-slate-800'}>Déficit Total: {data.totalDeficit} MW</h2>
            </div>
            <div className={'flex flex-col space-y-4'}>
                <div className={'w-fit'}>
                    <h1 className={'text-xl font-bold mt-20'}>Provincias</h1>
                    <div className={'h-1 w-full rounded-full bg-indigo-700'}/>
                </div>
                <div className={'grid grid-cols-3 gap-x-4 gap-y-10'}>
                    {data.provinces.map((province, index) => (
                        <div key={index}
                             className={'flex flex-col space-y-2 p-5 border-2 bg-indigo-50 border-indigo-600 rounded-md'}>
                            <h3 className={'text-lg font-bold text-slate-800'}>{province.name}</h3>
                            <div className={'flex flex-col space-y-2'}>
                                <h4 className={'text-base font-semibold text-slate-800'}>Demanda: {province.demand} MW</h4>
                                <h4 className={'text-base font-semibold text-slate-800'}>Asignado: {province.assigned} MW</h4>
                                <h4 className={'text-base font-semibold text-slate-800'}>Déficit: {province.deficit} MW</h4>
                                <h4 className={'text-base font-semibold text-slate-800'}>Horas de
                                    corte: {province.powerCutHours} h</h4>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <div className={'flex flex-col justify-center items-center mt-16'}>
                <div>
                    <h1 className={'text-xl font-bold'}>Gráficos</h1>
                    <div className={'h-1 w-full rounded-full bg-indigo-700'}/>
                </div>
                <div className={'flex mt-5'}>
                    <img className={'w-1/2 p-5'} src={`http://localhost:5000/static/optimization_result.png`}
                         alt={'chart'}/>
                    <img className={'w-1/2 p-5'} src={`http://localhost:5000/static/power-cut-hour.png`}
                         alt={'hour'}/>
                </div>
            </div>
        </div>
    )
}