import CubaMapImg from "/src/assets/cuba-map.png"
import ArtemisaImg from "/src/assets/artemisa.png"
import ProvinceCard from "./components/ProvinceCard.tsx";
import {useState} from "react";
import {ITermoelectrica, IProvinceDemand} from "./interfaces/types.ts";
import TorreImg from "/src/assets/tower.svg"
import StarsImg from "/src/assets/stars.png"
import {useServerGenerate} from "./hooks/useServerGenerate.ts";

const provinceDataInit: IProvinceDemand[] = [
    {
        name: "Pinar del Río",
        demand: 0,
    },
    {
        name: "Artemisa",
        demand: 0,
    },

    {
        name: "La Habana",
        demand: 0,
    },
    {
        name: "Mayabeque",
        demand: 0,
    },
    {
        name: "Matanzas",
        demand: 0,
    },
    {
        name: "Cienfuegos",
        demand: 0,
    },
    {
        name: "Villa Clara",
        demand: 0,
    },
    {
        name: "Sancti Spíritus",
        demand: 0,
    },
    {
        name: "Ciego de Ávila",
        demand: 0,
    },
    {
        name: "Camagüey",
        demand: 0,
    },

    {
        name: "Las Tunas",
        demand: 0,
    },

    {
        name: "Holguín",
        demand: 0,
    },
    {
        name: "Granma",
        demand: 0,
    },
    {
        name: "Santiago de Cuba",
        demand: 0,
    },
    {
        name: "Guantánamo",
        demand: 0,
    },

]
interface IProvinceImgMapper {
    [key: string]: string;
}
const provinceImgMapper: IProvinceImgMapper = {
    ["Pinar del Río"]: ArtemisaImg,
    ["Artemisa"]: ArtemisaImg,
    ["La Habana"]: ArtemisaImg,
    ["Mayabeque"]: ArtemisaImg,
    ["Matanzas"]: ArtemisaImg,
    ["Cienfuegos"]: ArtemisaImg,
    ["Villa Clara"]: ArtemisaImg,
    ["Sancti Spíritus"]: ArtemisaImg,
    ["Ciego de Ávila"]: ArtemisaImg,
    ["Camagüey"]: ArtemisaImg,
    ["Las Tunas"]: ArtemisaImg,
    ["Holguín"]: ArtemisaImg,
    ["Granma"]: ArtemisaImg,
    ["Santiago de Cuba"]: ArtemisaImg,
    ["Guantánamo"]: ArtemisaImg,
}

function App() {
    const [provincesData, setProvincesData] = useState<IProvinceDemand[]>(provinceDataInit);
    const {executeGenerate, isGenerating, dataGenerated} = useServerGenerate()
    const updateDemand = (index: number, newDemand: number) => {
        const updatedProvinces = provincesData.map((province, i) =>
            i === index ? { ...province, demand: newDemand } : province
        );
        setProvincesData(updatedProvinces);
    };
    const [termoelectricas, setTermoelectricas] = useState<ITermoelectrica[]>([])
    const updateGeneration = (index: number, newGeneration: number) => {
        const updatedTermoelectricas = termoelectricas.map((termoelectrica, i) =>
            i === index ? { ...termoelectrica, generationPerDay: newGeneration } : termoelectrica
        );
        setTermoelectricas(updatedTermoelectricas);
    }
    const updateName = (index: number, newName: string) => {
        const updatedTermoelectricas = termoelectricas.map((termoelectrica, i) =>
            i === index ? { ...termoelectrica, name: newName } : termoelectrica
        );
        setTermoelectricas(updatedTermoelectricas);
    }

    const generate = () => {
        executeGenerate(provincesData, termoelectricas)
    }
    return (
        <div className={'h-dvh bg-slate-50 px-10 pb-30 overflow-y-scroll'}>
            <div className={'flex flex-col items-center'}>
                <img className={'w-1/3'} src={CubaMapImg} alt={'Cuba'}/>
                <div>
                    <h1 className={'font-bold text-xl text-slate-800'}>Demanda</h1>
                    <div className={'h-1 w-full rounded-full bg-indigo-700'}/>
                </div>
                <div className={'w-full grid lg:grid-cols-4 grid-cols-2 mt-5 gap-5'}>
                    {provincesData.map((item, index) => {
                        return (
                            <ProvinceCard
                                key={index}
                                img={provinceImgMapper[item.name]}
                                name={item.name}
                                demand={item.demand}
                                setDemand={(newDemand) => updateDemand(index, newDemand)}
                            />
                        );
                    })}
                </div>
                <div>
                    <h1 className={'text-xl font-bold mt-10'}>Generación</h1>
                    <div className={'h-1 w-full rounded-full bg-indigo-700'}/>
                </div>
                <div className={'grid lg:grid-cols-4 md:grid-cols-3 grid-cols-2 mt-5 gap-5 w-full'}>
                    {termoelectricas.map((item, index) => {
                        return (
                            <div className={'flex h-fit space-x-2 p-2 rounded-lg'}>
                                <div className={'px-2'}>
                                    <img src={TorreImg} alt={'Artemisa'} className={'h-full w-10'}/>
                                </div>
                                <div className={'flex-col flex h-full pe-2 space-y-2'}>
                                    <input
                                        className={'font-semibold text-slate-800 mt-1 h-full w-18 bg-slate-100 rounded-md p-1 w-full hover:ring-0 hover:ring-transparent'}
                                        placeholder={'Nombre'}
                                        type={"text"}
                                        value={item.name}
                                        onChange={(e) => updateName(index, e.target.value)}
                                    />
                                    <div className={'flex items-center space-x-2'}>
                                        <p className={'text-sm text-slate-600 font-semibold'}>Demanda Promedio: </p>
                                        <input
                                            className={'h-full w-18 bg-slate-100 rounded-md p-1'}
                                            placeholder={'0'}
                                            type={"number"}
                                            min={0}
                                            value={item.generationPerDay === 0 ? '' : item.generationPerDay}
                                            onChange={(e) => updateGeneration(index, Number(e.target.value))}
                                        />
                                        <p className={'text-xs self-end font-semibold text-slate-600'}>MW</p>
                                    </div>
                                </div>
                            </div>
                        )
                    })
                    }
                    <button
                        className={'border-indigo-600 border-3 rounded-lg px-5 py-2 text-indigo-600 font-semibold hover:bg-indigo-100 hover:cursor-pointer'}
                        onClick={() => setTermoelectricas([...termoelectricas, {name: '', generationPerDay: 0}])}
                    >
                        Nueva termoeléctrica
                    </button>
                </div>
            </div>
            <div className={'mt-20 flex justify-center items-center'}>
                <div className={'h-1 w-full rounded-full bg-indigo-700'}/>
                <h1 className={'text-xl font-bold mx-5 text-slate-900 text-center'}>Modelo</h1>
                <div className={'h-1 w-full rounded-full bg-indigo-700'}/>

            </div>
            <div className={'mt-10'}>
                <p className={'italic text-slate-600 font-thin mt-10'}>Aún no hay datos, presione el botón de generar</p>
            </div>
            <button
                className={'group p-4  bg-indigo-200 shadow-indigo-200 shadow-lg flex justify-center items-center rounded-xl fixed end-16 bottom-20 hover:cursor-pointer hover:bg-indigo-300 transition-all'}
                onClick={generate}
            >
                <img src={StarsImg} alt={'Generar'} className={'size-12'}/>
                <p className={'transition-all text-slate-800 font-bold text-lg overflow-clip group-hover:w-20 w-0'}>Generar</p>

            </button>
        </div>
    );
}

export default App
