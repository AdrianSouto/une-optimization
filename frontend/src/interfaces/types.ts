export interface IProvinceDemand {
    name: string,
    demand: number
}
export interface ITermoelectrica {
    name: string,
    generationPerDay: number
}

export interface IProvinceResponse {
    id: number
    name: string
    demand: number
    assigned: number
    deficit: number
    powerCutHours: number
}
export interface IBlockEnergyDetailsResponse{
    block: number
    consumoPromedioBloques: number
    energiaAsignada: number
    energiaConsumida: number
    horasEncendido: number
    intervals: [[number, number]]
}


export interface IServerDataResponse {
    provinces: IProvinceResponse[]
    totalDemand: number
    totalGeneration: number
    totalDeficit: number
    blockEnergyDetails: IBlockEnergyDetailsResponse[]
}

export interface ISchedulerResponse {
    chartUrl: string
    schedule: ISchedule[]
}

export interface ISchedule {
    blockNumber: number
    schedule: {
        dayOfWeek: number
        startCut: number
        endCut: number
    }[]
}