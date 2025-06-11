import {useState} from "react";

interface Props{
    img: string,
    name: string,
    selected: boolean
    setSelected: () => void
    setBlockQuantity: (block: number) => void
    onClick: React.MouseEventHandler<HTMLDivElement>
    error: boolean
    setError: (error: boolean) => void
}

export default function ProvinceCard({img, name, selected, setBlockQuantity, onClick, error, setError, setSelected }: Props){
    const [blockQ, setBlockQ] = useState(0)
    return (
        <div className={`transition-all flex justify-around space-x-2 p-2 rounded-lg ${selected? 'ring-2 ring-indigo-500' : 'cursor-pointer'} ${error? 'ring-red-500' : ''}`}
            onClick={(e) => {
                if (!selected) {
                    setBlockQuantity(blockQ)
                    setError(false)
                    setSelected()
                }

                onClick(e)
            }}

        >
            <img src={img} alt={'Artemisa'} className={'h-14 w-20'}/>
            <div className={'flex-col flex h-full justify-between'}>
                <h2 className={'font-bold text-slate-800 mt-1'}>{name}</h2>
                {selected &&
                    <div className={'flex space-x-2 items-center'}>
                        <label className={'font-semibold text-sm'}>Cant. bloques:</label>
                        <input
                            className={`h-full w-18 bg-slate-100 rounded-md p-1 text-sm font-semibold ${error? 'ring ring-red-500' : ''}`}
                            placeholder={'0'}
                            type={"number"}
                            min={1}
                            value={blockQ === 0 ? '' : blockQ}
                            onChange={(e) => {
                                setBlockQ(Number(e.target.value))
                                setBlockQuantity(Number(e.target.value))
                                setError(false)
                            }}
                        />
                    </div>

                }

            </div>
        </div>
    )
}