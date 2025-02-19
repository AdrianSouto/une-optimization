import {useState} from "react";
import {IProvinceDemand, ITermoelectrica} from "../interfaces/types.ts";

interface IProvinceResponse {
    id: number
    name: string
    demand: number
    assigned: number
    deficit: number
    powerCutHours: number
}

interface IGenerateData {
    provinces: IProvinceResponse[]
    totalDemand: number
    totalGeneration: number
    totalDeficit: number
    chartUrl: string
}

export function useServerGenerate(){
    const [isGenerating, setIsGenerating] = useState(false)
    const [dataGenerated, setDataGenerated] = useState<IGenerateData>()

    const executeGenerate = (provincesDemand: IProvinceDemand[], termoelectricas: ITermoelectrica[], blockDemand: number[]) => {
        setIsGenerating(true)
        fetch("http://localhost:5000/api/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                provincesDemand,
                termoelectricas,
                blockDemand
            })
        })
        .then(response => response.json())
        .then(data => {
            setDataGenerated(data)
            setIsGenerating(false)
        })

    }

    return {
        isGenerating,
        dataGenerated,
        executeGenerate
    }
}