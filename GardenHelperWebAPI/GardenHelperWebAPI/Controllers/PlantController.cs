using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using GardenHelperWebAPI.Data;
using GardenHelperWebAPI.Models;


namespace GardenHelperWebAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PlantController : ControllerBase
    {
        private ApplicationDbContext _context;
        public PlantController(ApplicationDbContext context)
        {
            _context = context;
        }
        // GET Plants in database
        [HttpGet]
        public IActionResult Get()
        {
            var plants = _context.Plants;
            return Ok(plants);
        }
        // GET Plants By Gardener
        [HttpGet("gardener={gardener_id}/index")]
        public IActionResult Get(int gardener_id)
        {
            var plant = _context.Plants.Where(m => m.GardenerId == gardener_id);
            return Ok(plant);
        }
        // GET Gardener Details
        [HttpGet("gardener={gardener_id}")]
        public IActionResult GetGardener(int gardener_id)
        {
            var gardener = _context.Gardeners.Where(m => m.Id == gardener_id);
            return Ok(gardener);
        }

        [HttpGet("gardener={gardener_id}/plant={id}")]
        public IActionResult Get(int id, int gardener_id)
        {
            var plant = _context.Plants.Where(m => m.Id == id && m.GardenerId == gardener_id);
            return Ok(plant);
        }

        
        [HttpPost]
        public IActionResult Post([FromBody] Plant value)
        {
            _context.Plants.Add(value);
            _context.SaveChanges();
            return Ok();
        }

        // PUT api/movie
        [HttpPut]
        public IActionResult Put([FromBody] Plant plant)
        {
            _context.Plants.Update(plant);
            _context.SaveChanges();
            return Ok();
        }

        
        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            var selectedPlant = _context.Plants.FirstOrDefault(m => m.Id == id);
            _context.Plants.Remove(selectedPlant);
            _context.SaveChanges();
            return Ok();
        }
    }
}
