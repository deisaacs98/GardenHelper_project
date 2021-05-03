using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GardenStatsWebAPI.Models
{
    public class EdibleLog
    {
        public int Id { get; set; }
        public double PlantId { get; set; }
        public string Date { get; set; }
        public int Quality { get; set; }
        public bool Harvested { get; set; }
        public int DaysToHarvest { get; set; }
        public double AmountHarvested { get; set; }


    }
}
