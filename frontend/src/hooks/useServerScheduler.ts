import {useState} from "react";
import {IProvinceDemand, ISchedulerResponse} from "../interfaces/types.ts";


export function useServerScheduler(){
    const [isScheduling, setIsScheduling] = useState(false)
    const [schedule, setSchedule] = useState<ISchedulerResponse>()

    const generateScheduler = (provinceDemand: IProvinceDemand, blocksQuantity: number) => {
        setIsScheduling(true)
        fetch("http://localhost:5000/api/schedule", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                provinceDemand,
                blocksQuantity,
            })
        })
        .then(response => response.json())
        .then(data => {
            setSchedule(data)
        })
        setIsScheduling(false)
    }

    return {
        isScheduling,
        schedule,
        generateScheduler
    }
}