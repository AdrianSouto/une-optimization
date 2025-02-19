interface Props{
    img: string,
    name: string,
    demand: number
    setDemand: (demand: number) => void
}

export default function ProvinceCard({img, name, demand, setDemand}: Props){
    return (
        <div className={'flex h-fit space-x-2 p-2 rounded-lg'}>
            <img src={img} alt={'Artemisa'} className={'size-fit'}/>
            <div className={'flex-col flex h-full pe-2'}>
                <h2 className={'font-bold text-slate-800 mt-1'}>{name}</h2>
                <div className={'flex items-center space-x-2'}>
                    <p className={'text-sm text-slate-600 font-semibold'}>Demanda Promedio: </p>
                    <input
                        className={'h-full w-18 bg-slate-100 rounded-md p-1'}
                        placeholder={'0'}
                        type={"number"}
                        min={0}
                        value={demand === 0 ? '' : demand}
                        onChange={(e) => setDemand(Number(e.target.value))}
                    />
                    <p className={'text-xs self-end font-semibold text-slate-600'}>MW</p>
                </div>
            </div>
        </div>
    )
}