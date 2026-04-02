# services.py
# All 5 services and their subservices for Samriddhi Anveshana
# Edit this file to add, remove, or rename services/subservices

SERVICES = {
    "1": {
        "name": "IT Services & Digital Infrastructure",
        "emoji": "🖥️",
        "subservices": {
            "1": "Hospital Management System (HMS) implementation",
            "2": "Electronic Medical Records (EMR/EHR)",
            "3": "Cloud infrastructure setup",
            "4": "Data security & cybersecurity",
            "5": "Server & network management",
            "6": "Telemedicine platform integration",
            "7": "Appointment booking systems",
            "8": "IT support & maintenance",
        }
    },
    "2": {
        "name": "Digital Marketing",
        "emoji": "📣",
        "subservices": {
            "1": "Hospital website development",
            "2": "Search Engine Optimisation (SEO)",
            "3": "Google & Meta advertising",
            "4": "Social media management",
            "5": "Marketing Analytics & Performance Optimization",
            "6": "Patient engagement campaigns",
            "7": "Healthcare content creation",
            "8": "Doctor branding & promotion",
        }
    },
    "3": {
        "name": "24×7 Operational Support",
        "emoji": "🔄",
        "subservices": {
            "1": "IT monitoring",
            "2": "Digital marketing monitoring",
            "3": "Patient engagement tools",
            "4": "Data reporting dashboards",
            "5": "Emergency technical support",
        }
    },
    "4": {
        "name": "Compliance & Regulatory Services",
        "emoji": "📋",
        "subservices": {
            "1": "Healthcare regulatory compliance",
            "2": "Data privacy compliance",
            "3": "NABH/NABL documentation assistance",
            "4": "Operational compliance systems",
            "5": "Audit preparation",
            "6": "Policy documentation",
            "7": "Legal & administrative support",
        }
    },
    "5": {
        "name": "Operational Consulting",
        "emoji": "📊",
        "subservices": {
            "1": "Hospital workflow optimization",
            "2": "Patient journey improvement",
            "3": "Operational cost reduction",
            "4": "Vendor management systems",
            "5": "Resource planning",
            "6": "Performance analytics",
        }
    },
}


def build_main_menu() -> str:
    """Builds the main services menu message string."""
    lines = [
        "👋 *Welcome to Samriddhi Anveshana!*",
        "🏥 Your trusted healthcare growth partner, Hyderabad.\n",
        "Please choose a service:\n",
    ]
    for key, svc in SERVICES.items():
        lines.append(f"{svc['emoji']} {key}. {svc['name']}")
    lines.append("\n🧑 6. Talk to our team directly")
    lines.append("\nReply with a number to continue.")
    return "\n".join(lines)


def build_service_menu(service_id: str) -> str:
    """Builds the subservices menu for a given service ID."""
    svc = SERVICES[service_id]
    lines = [
        f"{svc['emoji']} *{svc['name']}*\n",
        "Choose a subservice:\n"
    ]
    for key, name in svc["subservices"].items():
        lines.append(f"  {key}. {name}")
    lines.append("\n0. 🔙 Back to main menu")
    return "\n".join(lines)
