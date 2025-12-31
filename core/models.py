"""
Data Models

Data classes for API responses and domain objects.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional


@dataclass
class Address:
    """Address information"""

    navn: str
    vejnavn: str
    husnummer: str
    etage: Optional[str]
    sidedør: Optional[str]
    postdistrikt: str
    postnummer: str
    kvhxcode: str
    kommunenummer: int
    vejkode: int
    breddegrad: float
    laengdegrad: float

    @classmethod
    def from_dict(cls, data: dict) -> "Address":
        """Create Address from dictionary"""
        return cls(
            navn=data.get("navn", ""),
            vejnavn=data.get("vejnavn", ""),
            husnummer=data.get("husnummer", ""),
            etage=data.get("etage"),
            sidedør=data.get("sidedør"),
            postdistrikt=data.get("postdistrikt", ""),
            postnummer=data.get("postnummer", ""),
            kvhxcode=data.get("kvhxcode", ""),
            kommunenummer=data.get("kommunenummer", 0),
            vejkode=data.get("vejkode", 0),
            breddegrad=data.get("breddegrad", 0.0),
            laengdegrad=data.get("laengdegrad", 0.0),
        )


@dataclass
class Standplads:
    """Collection point (waste bin location)"""

    nummer: str
    navn: str
    beskrivelse: Optional[str]
    adresse: Address
    længdegrad: float
    breddegrad: float
    sidstændret: datetime
    beholder: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Standplads":
        """Create Standplads from dictionary"""
        # Parse datetime
        sidstændret_str = data.get("sidstændret", "")
        try:
            sidstændret = datetime.fromisoformat(sidstændret_str.replace("Z", "+00:00"))
        except Exception:
            sidstændret = datetime.now()

        return cls(
            nummer=data.get("nummer", ""),
            navn=data.get("navn", ""),
            beskrivelse=data.get("beskrivelse"),
            adresse=Address.from_dict(data.get("adresse", {})),
            længdegrad=data.get("længdegrad", 0.0),
            breddegrad=data.get("breddegrad", 0.0),
            sidstændret=sidstændret,
            beholder=data.get("beholder"),
        )


@dataclass
class PlannedCollection:
    """Planned waste collection"""

    dato: datetime
    fraktioner: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> "PlannedCollection":
        """Create PlannedCollection from dictionary"""
        # Parse datetime
        dato_str = data.get("dato", "")
        try:
            dato = datetime.fromisoformat(dato_str.replace("Z", "+00:00"))
        except Exception:
            dato = datetime.now()

        return cls(dato=dato, fraktioner=data.get("fraktioner", []))

    def get_date_str(self) -> str:
        """Get formatted date string - shows 'i dag' for today, 'i morgen' for tomorrow"""
        today = datetime.now().date()
        collection_date = self.dato.date()

        if collection_date == today:
            return "i dag"
        elif collection_date == today + timedelta(days=1):
            return "i morgen"
        else:
            return self.dato.strftime("%Y-%m-%d")

    def get_fractions_str(self) -> str:
        """Get comma-separated fractions string"""
        return ", ".join(self.fraktioner)


@dataclass
class WasteSchedule:
    """Complete waste collection schedule for a location"""

    standplads: Standplads
    planlagtetømninger: List[PlannedCollection]

    @classmethod
    def from_dict(cls, data: dict) -> "WasteSchedule":
        """Create WasteSchedule from dictionary"""
        standplads = Standplads.from_dict(data.get("standplads", {}))

        planlagt = data.get("planlagtetømninger", [])
        planlagtetømninger = [PlannedCollection.from_dict(p) for p in planlagt]

        return cls(standplads=standplads, planlagtetømninger=planlagtetømninger)

    def get_next_collection(self) -> Optional[PlannedCollection]:
        """Get the next upcoming collection (including today)"""
        today = datetime.now(timezone.utc).date()
        upcoming = [c for c in self.planlagtetømninger if c.dato.date() >= today]

        if upcoming:
            return min(upcoming, key=lambda c: c.dato)
        return None

    def get_collections_for_date(self, target_date: datetime) -> List[PlannedCollection]:
        """Get all collections for a specific date"""
        target_date_str = target_date.strftime("%Y-%m-%d")
        return [
            c for c in self.planlagtetømninger if c.dato.strftime("%Y-%m-%d") == target_date_str
        ]
