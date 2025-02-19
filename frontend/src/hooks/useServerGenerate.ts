import {useState} from "react";
import {IProvinceDemand, IServerDataResponse, ITermoelectrica} from "../interfaces/types.ts";


export function useServerGenerate(){
    const [isGenerating, setIsGenerating] = useState(false)
    const [dataGenerated, setDataGenerated] = useState<IServerDataResponse>()

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